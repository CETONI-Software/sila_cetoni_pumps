from __future__ import annotations

import math
import time
from concurrent.futures import Executor
from threading import Event

from qmixsdk.qmixpump import Pump
from sila2.framework.errors.validation_error import ValidationError
from sila2.server import MetadataDict, SilaServer

from sila_cetoni.application.system import ApplicationSystem, requires_operational_system

from ..generated.syringeconfigurationcontroller import (
    SetSyringeParameters_Responses,
    SyringeConfigurationControllerBase,
    SyringeConfigurationControllerFeature,
)


class SyringeConfigurationControllerImpl(SyringeConfigurationControllerBase):
    __pump: Pump
    __system: ApplicationSystem
    __stop_event: Event

    def __init__(self, server: SilaServer, pump: Pump, executor: Executor):
        super().__init__(server)
        self.__pump = pump
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        def update_inner_diameter(stop_event: Event):
            new_inner_diameter = inner_diameter = self.__pump.get_syringe_param().inner_diameter_mm
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_inner_diameter = self.__pump.get_syringe_param().inner_diameter_mm
                if not math.isclose(new_inner_diameter, inner_diameter):
                    inner_diameter = new_inner_diameter
                    self.update_InnerDiameter(inner_diameter)
                time.sleep(0.1)

        def update_max_piston_stroke(stop_event: Event):
            new_max_piston_stroke = max_piston_stroke = self.__pump.get_syringe_param().max_piston_stroke_mm
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_max_piston_stroke = self.__pump.get_syringe_param().max_piston_stroke_mm
                if not math.isclose(new_max_piston_stroke, max_piston_stroke):
                    max_piston_stroke = new_max_piston_stroke
                    self.update_MaxPistonStroke(max_piston_stroke)
                time.sleep(0.1)

        # initial values
        self.update_InnerDiameter(self.__pump.get_syringe_param().inner_diameter_mm)
        self.update_MaxPistonStroke(self.__pump.get_syringe_param().max_piston_stroke_mm)

        executor.submit(update_inner_diameter, self.__stop_event)
        executor.submit(update_max_piston_stroke, self.__stop_event)

    @requires_operational_system(SyringeConfigurationControllerFeature)
    def SetSyringeParameters(
        self, InnerDiameter: float, MaxPistonStroke: float, *, metadata: MetadataDict
    ) -> SetSyringeParameters_Responses:
        def _validate(value: float, parameter: str, parameter_id: int):
            if value < 0:
                err = ValidationError(f"The {parameter} ({value}) is invalid. It cannot be less than 0!")
                err.parameter_fully_qualified_identifier = (
                    SyringeConfigurationControllerFeature["SetSyringeParameters"]
                    .parameters.fields[parameter_id]
                    .fully_qualified_identifier
                )
                raise err

        _validate(InnerDiameter, "InnerDiameter", 0)
        _validate(MaxPistonStroke, "MaxPistonStroke", 1)
        self.__pump.set_syringe_param(InnerDiameter, MaxPistonStroke)

    def stop(self) -> None:
        super().stop()
        self.__stop_event.set()
