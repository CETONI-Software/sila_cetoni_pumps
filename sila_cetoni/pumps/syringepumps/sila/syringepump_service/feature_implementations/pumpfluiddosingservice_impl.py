# Generated by sila2.code_generator; sila2.__version__: 0.10.1
from __future__ import annotations

import datetime
import logging
import math
import time

from qmixsdk.qmixbus import PollingTimer
from qmixsdk.qmixpump import Pump
from sila2.server import MetadataDict, ObservableCommandInstance, SilaServer

from sila_cetoni.application.system import ApplicationSystem, CetoniApplicationSystem
from sila_cetoni.utils import PropertyUpdater, negate

from .....validate import validate
from ..generated.pumpfluiddosingservice import (
    DoseVolume_Responses,
    GenerateFlow_Responses,
    PumpFluidDosingServiceBase,
    PumpFluidDosingServiceFeature,
    PumpIsInFaultState,
    PumpIsNotEnabled,
    SetFillLevel_Responses,
    StopDosage_Responses,
)

logger = logging.getLogger(__name__)


@CetoniApplicationSystem.monitor_traffic
class PumpFluidDosingServiceImpl(PumpFluidDosingServiceBase):
    __pump: Pump
    __system: ApplicationSystem

    def __init__(self, server: SilaServer, pump: Pump):
        super().__init__(server)
        self.__pump = pump
        self.__system = ApplicationSystem()

        not_close = negate(math.isclose)

        self.run_periodically(
            PropertyUpdater(
                lambda: self.__pump.get_flow_is() if self.__system.state.is_operational() else 0,
                not_close,
                self.update_FlowRate,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                self.__pump.get_flow_rate_max,
                not_close,
                self.update_MaxFlowRate,
                when=self.__system.state.is_operational,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                lambda: self.__pump.get_fill_level() if self.__system.state.is_operational() else 0,
                not_close,
                self.update_SyringeFillLevel,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                self.__pump.get_volume_max,
                not_close,
                self.update_MaxSyringeFillLevel,
                when=self.__system.state.is_operational,
            )
        )

    def __ensure_enabled(self):
        """
        Checks that the pump drive is enabled and not in a fault state. Raises the appropriate error if not.
        """
        if self.__pump.is_in_fault_state():
            raise PumpIsInFaultState()
        if not self.__pump.is_enabled():
            raise PumpIsNotEnabled()

    @ApplicationSystem.ensure_operational(PumpFluidDosingServiceFeature)
    def StopDosage(self, *, metadata: MetadataDict) -> StopDosage_Responses:
        self.__pump.stop_pumping()

    def _wait_dosage_finished(self, instance: ObservableCommandInstance):
        """
        The function waits until the last dosage command has finished or
        until a timeout occurs. The timeout is estimated from the dosage's flow
        and target volume
        """

        if not self.__pump.is_pumping():
            return

        target_volume = self.__pump.get_target_volume()
        logger.debug("target volume: %f, current volume: %f", target_volume, self.__pump.get_fill_level())
        if math.isclose(target_volume, 0, abs_tol=1e-05):
            return

        flow_in_sec = self.__pump.get_flow_is() / self.__pump.get_flow_unit().time_unitid.value
        if flow_in_sec == 0:
            # try again, maybe the pump didn't start pumping yet
            time.sleep(0.5)
            flow_in_sec = self.__pump.get_flow_is() / self.__pump.get_flow_unit().time_unitid.value
        if flow_in_sec == 0:
            raise RuntimeError(f"The pump didn't start pumping. Last error: {self.__pump.read_last_error()}")

        logger.debug("flow_in_sec: %f", flow_in_sec)
        dosing_time = datetime.timedelta(seconds=self.__pump.get_target_volume() / flow_in_sec + 2)  # +2 sec buffer
        logger.debug("dosing_time_s: %fs", dosing_time.seconds)

        timer = PollingTimer(period_ms=dosing_time.seconds * 1000)
        message_timer = PollingTimer(period_ms=500)
        is_pumping = True
        POLLING_TIMEOUT = datetime.timedelta(seconds=0.1)
        while is_pumping and not timer.is_expired():
            time.sleep(POLLING_TIMEOUT.total_seconds())
            dosing_time -= POLLING_TIMEOUT
            if message_timer.is_expired():
                logger.info("Fill level: %s", self.__pump.get_fill_level())
                instance.progress = min(self.__pump.get_dosed_volume() / target_volume, 1)
                instance.estimated_remaining_time = dosing_time
                message_timer.restart()
            is_pumping = self.__pump.is_pumping()

        if is_pumping or self.__pump.is_in_fault_state() or not self.__pump.is_enabled():
            raise RuntimeError(f"An unexpected error occurred: {self.__pump.read_last_error()}")

    @ApplicationSystem.ensure_operational(PumpFluidDosingServiceFeature)
    def SetFillLevel(
        self,
        FillLevel: float,
        FlowRate: float,
        *,
        metadata: MetadataDict,
        instance: ObservableCommandInstance,
    ) -> SetFillLevel_Responses:
        self.__ensure_enabled()
        validate(
            self.__pump,
            PumpFluidDosingServiceFeature["SetFillLevel"],
            FlowRate,
            1,
            fill_level=FillLevel,
            fill_level_id=0,
        )
        self.__pump.stop_pumping()  # only one dosage allowed
        time.sleep(0.25)  # wait for the currently running dosage to catch up

        self.__pump.set_fill_level(FillLevel, FlowRate)
        self._wait_dosage_finished(instance)

    @ApplicationSystem.ensure_operational(PumpFluidDosingServiceFeature)
    def DoseVolume(
        self,
        Volume: float,
        FlowRate: float,
        *,
        metadata: MetadataDict,
        instance: ObservableCommandInstance,
    ) -> DoseVolume_Responses:
        self.__ensure_enabled()
        validate(self.__pump, PumpFluidDosingServiceFeature["DoseVolume"], FlowRate, 1, volume=Volume, volume_id=0)
        self.__pump.stop_pumping()  # only one dosage allowed
        time.sleep(0.25)  # wait for the currently running dosage to catch up

        self.__pump.pump_volume(Volume, FlowRate)
        self._wait_dosage_finished(instance)

    @ApplicationSystem.ensure_operational(PumpFluidDosingServiceFeature)
    def GenerateFlow(
        self, FlowRate: float, *, metadata: MetadataDict, instance: ObservableCommandInstance
    ) -> GenerateFlow_Responses:
        # `FlowRate` is negative to indicate aspiration of fluid.
        # Since `validate` tests against 0 and the max flow rate of the pump, we pass the absolute value of `FlowRate`.
        self.__ensure_enabled()
        validate(self.__pump, PumpFluidDosingServiceFeature["GenerateFlow"], abs(FlowRate), 0)
        self.__pump.stop_pumping()  # only one dosage allowed
        time.sleep(0.25)  # wait for the currently running dosage to catch up

        self.__pump.generate_flow(FlowRate)
        self._wait_dosage_finished(instance)
