from __future__ import annotations

import time

from qmixsdk.qmixpump import ContiFlowPump
from sila2.server import MetadataDict, ObservableCommandInstance, SilaServer

from sila_cetoni.utils import PropertyUpdater, not_close

from .....validate import validate
from ..generated.continuousflowdosingservice import (
    ContinuousFlowDosingServiceBase,
    ContinuousFlowDosingServiceFeature,
    GenerateFlow_Responses,
    StopDosage_Responses,
)


class ContinuousFlowDosingServiceImpl(ContinuousFlowDosingServiceBase):
    __pump: ContiFlowPump

    def __init__(self, server: SilaServer, pump: ContiFlowPump):
        super().__init__(server)
        self.__pump = pump

        self.run_periodically(
            PropertyUpdater(
                self.__pump.get_flow_is,
                not_close,
                self.update_FlowRate,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                self.__pump.get_flow_rate_max,
                not_close,
                self.update_MaxFlowRate,
            )
        )

    def StopDosage(self, *, metadata: MetadataDict) -> StopDosage_Responses:
        self.__pump.stop_pumping()

    def GenerateFlow(
        self, FlowRate: float, *, metadata: MetadataDict, instance: ObservableCommandInstance
    ) -> GenerateFlow_Responses:
        validate(self.__pump, ContinuousFlowDosingServiceFeature["GenerateFlow"], FlowRate)
        # self.__pump.stop_pumping() # only one dosage allowed
        # time.sleep(0.25) # wait for the currently running dosage to catch up

        self.__pump.generate_flow(FlowRate)

        instance.begin_execution()

        is_pumping = True
        while is_pumping:
            time.sleep(0.5)
            is_pumping = self.__pump.is_pumping()

        if is_pumping or self.__pump.is_in_fault_state():
            raise RuntimeError(
                f"Pump is in fault state. The last error that occurred was {self.__pump.read_last_error()!r}"
            )
