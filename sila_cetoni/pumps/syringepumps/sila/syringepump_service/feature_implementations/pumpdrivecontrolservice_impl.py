# Generated by sila2.code_generator; sila2.__version__: 0.10.1
from __future__ import annotations

import datetime
import logging
import time
from queue import Queue
from typing import Optional

from qmixsdk.qmixbus import DeviceError, PollingTimer
from qmixsdk.qmixpump import Pump
from sila2.server import MetadataDict, ObservableCommandInstance, SilaServer

from sila_cetoni.application.server_configuration import ServerConfiguration
from sila_cetoni.application.system import ApplicationSystem, CetoniApplicationSystem
from sila_cetoni.utils import PropertyUpdater, not_equal

from ..generated.pumpdrivecontrolservice import (
    DisablePumpDrive_Responses,
    EnablePumpDrive_Responses,
    InitializationFailed,
    InitializationNotFinished,
    InitializePumpDrive_Responses,
    NotSupported,
    PumpDriveControlServiceBase,
    PumpDriveControlServiceFeature,
    RestoreDrivePositionCounter_Responses,
)

logger = logging.getLogger(__name__)


@CetoniApplicationSystem.monitor_traffic
class PumpDriveControlServiceImpl(PumpDriveControlServiceBase):
    __pump: Pump
    __is_initializing: bool
    __system: ApplicationSystem
    __config: ServerConfiguration

    __CALIBRATION_TIMEOUT = datetime.timedelta(seconds=60)

    def __init__(self, server: SilaServer, pump: Pump):
        super().__init__(server)
        self.__pump = pump
        self.__is_initializing = False
        self.__system = ApplicationSystem()
        self.__config = ServerConfiguration(self.parent_server.server_name, self.__system.device_config.name)

        self.run_periodically(
            PropertyUpdater(
                self.__pump.is_in_fault_state,
                not_equal,
                self.update_FaultState,
                when=self.__system.state.is_operational,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                lambda: "Initializing"
                if self.__is_initializing
                else "Enabled"
                if self.__pump.is_enabled() and self.__system.state.is_operational()
                else "Disabled",
                not_equal,
                self.update_PumpDriveState,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                lambda: self.__pump.get_position_counter_value() if self.__system.state.is_operational() else 0,
                not_equal,
                self.update_DrivePositionCounter,
            )
        )
        self.run_periodically(self.__config.write, 60)

    def start(self) -> None:
        if not self.__pump.is_position_sensing_initialized():
            drive_pos_counter = self.__config["pump"].getint("drive_position_counter")
            if drive_pos_counter is not None:
                logger.debug(f"Restoring drive position counter: {drive_pos_counter}")
                self.__pump.restore_position_counter_value(drive_pos_counter)
            else:
                logger.warning(
                    f"Could not read drive position counter for {self.__pump.get_pump_name()} from config file. "
                    "Reference move needed!"
                )

        super().start()

    def stop(self) -> None:
        super().stop()
        self.__config.write()

    def update_DrivePositionCounter(self, DrivePositionCounter: int, queue: Optional[Queue[int]] = None):
        self.__config["pump"]["drive_position_counter"] = str(DrivePositionCounter)
        return super().update_DrivePositionCounter(DrivePositionCounter, queue)

    @ApplicationSystem.ensure_operational(PumpDriveControlServiceFeature)
    def EnablePumpDrive(self, *, metadata: MetadataDict) -> EnablePumpDrive_Responses:
        self.__pump.clear_fault()
        self.__pump.enable(True)

    @ApplicationSystem.ensure_operational(PumpDriveControlServiceFeature)
    def DisablePumpDrive(self, *, metadata: MetadataDict) -> DisablePumpDrive_Responses:
        self.__pump.enable(False)

    @ApplicationSystem.ensure_operational(PumpDriveControlServiceFeature)
    def RestoreDrivePositionCounter(
        self, DrivePositionCounterValue: int, *, metadata: MetadataDict
    ) -> RestoreDrivePositionCounter_Responses:
        try:
            self.__pump.restore_position_counter_value(DrivePositionCounterValue)
        except DeviceError as err:
            if err.errorcode == -0x00CA:  # -ERR_DEVNOSUPP
                raise NotSupported(str(err))
            raise

    @ApplicationSystem.ensure_operational(PumpDriveControlServiceFeature)
    def InitializePumpDrive(
        self, *, metadata: MetadataDict, instance: ObservableCommandInstance
    ) -> InitializePumpDrive_Responses:
        if self.__is_initializing:
            raise InitializationNotFinished()

        self.__is_initializing = True
        try:
            self.__pump.calibrate()
            time.sleep(0.2)
        except DeviceError as err:
            self.__is_initializing = False
            if err.args[1] == -212:
                # Device does not support this operation -> pump has an absolute encoder and does not need calibration
                return
            else:
                raise InitializationFailed(err.args[2] if len(err.args) > 2 else err.args[0])

        calibration_finished = self.__pump.is_calibration_finished() or not self.__pump.is_enabled()
        if calibration_finished:
            return

        timeout: datetime.timedelta = self.__CALIBRATION_TIMEOUT
        timer = PollingTimer(timeout.seconds * 1000)
        message_timer = PollingTimer(period_ms=500)
        POLLING_TIMEOUT = datetime.timedelta(seconds=0.1)
        while not (calibration_finished or timer.is_expired()):
            time.sleep(POLLING_TIMEOUT.total_seconds())
            timeout -= POLLING_TIMEOUT
            if message_timer.is_expired():
                instance.progress = (self.__CALIBRATION_TIMEOUT - timeout) / self.__CALIBRATION_TIMEOUT
                instance.estimated_remaining_time = timeout
                message_timer.restart()
            calibration_finished = self.__pump.is_calibration_finished()

        if not calibration_finished or self.__pump.is_in_fault_state():
            raise RuntimeError(f"An unexpected error occurred: {self.__pump.read_last_error()}")

        self.__is_initializing = False

        logger.info("Pump calibrated: %s", calibration_finished)
        last_error = self.__pump.read_last_error()
        if not calibration_finished and last_error.code != 0:
            raise InitializationFailed(
                f"The initialization did not end properly. The last error that occurred was {last_error}"
            )
