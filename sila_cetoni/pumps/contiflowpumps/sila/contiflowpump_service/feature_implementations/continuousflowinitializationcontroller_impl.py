from __future__ import annotations

import datetime
import time

from qmixsdk.qmixbus import PollingTimer
from qmixsdk.qmixpump import ContiFlowPump
from sila2.server import MetadataDict, ObservableCommandInstance, SilaServer

from sila_cetoni.utils import PropertyUpdater, not_equal

from ..generated.continuousflowinitializationcontroller import (
    ContinuousFlowInitializationControllerBase,
    InitializeContiflow_Responses,
)


class ContinuousFlowInitializationControllerImpl(ContinuousFlowInitializationControllerBase):
    __pump: ContiFlowPump

    def __init__(self, server: SilaServer, pump: ContiFlowPump):
        super().__init__(server)
        self.__pump = pump

        self.run_periodically(
            PropertyUpdater(
                self.__pump.is_initialized,
                not_equal,
                self.update_IsInitialized,
            )
        )

    def InitializeContiflow(
        self, *, metadata: MetadataDict, instance: ObservableCommandInstance
    ) -> InitializeContiflow_Responses:
        MAX_WAIT_TIME = datetime.timedelta(seconds=30)
        timer = PollingTimer(MAX_WAIT_TIME.seconds * 1000)

        self.__pump.initialize()

        while self.__pump.is_initializing() and not timer.is_expired():
            instance.estimated_remaining_time = datetime.timedelta(seconds=timer.get_msecs_to_expiration() / 1000)
            instance.progress = instance.estimated_remaining_time / MAX_WAIT_TIME  # type: ignore
            time.sleep(0.5)

        return InitializeContiflow_Responses()
