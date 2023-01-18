from __future__ import annotations

import logging
from collections import namedtuple
from concurrent.futures import Executor
from threading import Event
from typing import Any

from qmixsdk.qmixpump import Pump
from sila2.server import MetadataDict, SilaServer

from sila_cetoni.application.system import ApplicationSystem, CetoniApplicationSystem

from ..... import unit_conversion as uc
from ..generated.pumpunitcontroller import (
    PumpUnitControllerBase,
    PumpUnitControllerFeature,
    SetFlowUnit_Responses,
    SetVolumeUnit_Responses,
    VolumeUnit,
)

logger = logging.getLogger(__name__)


FlowUnit = namedtuple("FlowUnit", ["VolumeUnit", "TimeUnit"])


@CetoniApplicationSystem.monitor_traffic
class PumpUnitControllerImpl(PumpUnitControllerBase):
    __pump: Pump
    __system: ApplicationSystem
    __stop_event: Event

    def __init__(self, server: SilaServer, pump: Pump, executor: Executor):
        super().__init__(server)
        self.__pump = pump
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        def update_flow_unit(stop_event: Event):
            new_flow_unit = flow_unit = FlowUnit(*uc.flow_unit_to_tuple(self.__pump.get_flow_unit()))
            while not stop_event.wait(0.1):
                if self.__system.state.is_operational():
                    new_flow_unit = FlowUnit(*uc.flow_unit_to_tuple(self.__pump.get_flow_unit()))
                if new_flow_unit != flow_unit:
                    flow_unit = new_flow_unit
                    self.update_FlowUnit(flow_unit)

        def update_volume_unit(stop_event: Event):
            new_volume_unit = volume_unit = uc.volume_unit_to_string(self.__pump.get_volume_unit())
            while not stop_event.wait(0.1):
                if self.__system.state.is_operational():
                    new_volume_unit = uc.volume_unit_to_string(self.__pump.get_volume_unit())
                if new_volume_unit != volume_unit:
                    volume_unit = new_volume_unit
                    self.update_VolumeUnit(volume_unit)

        # initial values
        self.update_FlowUnit(FlowUnit(*uc.flow_unit_to_tuple(self.__pump.get_flow_unit())))
        self.update_VolumeUnit(uc.volume_unit_to_string(self.__pump.get_volume_unit()))

        executor.submit(update_flow_unit, self.__stop_event)
        executor.submit(update_volume_unit, self.__stop_event)

    @ApplicationSystem.ensure_operational(PumpUnitControllerFeature)
    def SetFlowUnit(self, FlowUnit: Any, *, metadata: MetadataDict) -> SetFlowUnit_Responses:
        logger.debug(f"flow unit {FlowUnit} {type(FlowUnit)}")

        # try:
        flow_unit = FlowUnit
        prefix, volume_unit, time_unit = uc.evaluate_units(
            parameter=PumpUnitControllerFeature["SetFlowUnit"].parameters.fields[0],
            requested_volume_unit=flow_unit.VolumeUnit,
            requested_time_unit=flow_unit.TimeUnit,
        )
        # except ValueError:
        #     err = ValidationError(
        #         "The given flow unit is malformed. It has to be something like 'ml/s', for instance."
        #     )
        #     err.parameter_fully_qualified_identifier = (
        #         PumpUnitControllerFeature["SetFlowUnit"].parameters.fields[0].fully_qualified_identifier
        #     )
        #     raise err
        # else:
        self.__pump.set_flow_unit(prefix, volume_unit, time_unit)

    @ApplicationSystem.ensure_operational(PumpUnitControllerFeature)
    def SetVolumeUnit(self, VolumeUnit: VolumeUnit, *, metadata: MetadataDict) -> SetVolumeUnit_Responses:
        prefix, volume_unit = uc.evaluate_units(
            parameter=PumpUnitControllerFeature["SetVolumeUnit"].parameters.fields[0], requested_volume_unit=VolumeUnit
        )
        self.__pump.set_volume_unit(prefix, volume_unit)

    def stop(self) -> None:
        super().stop()
        self.__stop_event.set()
