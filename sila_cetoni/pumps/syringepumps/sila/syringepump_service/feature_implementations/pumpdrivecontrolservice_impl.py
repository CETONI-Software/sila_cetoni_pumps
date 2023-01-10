from __future__ import annotations

import datetime
import logging
import time
from concurrent.futures import Executor
from queue import Queue
from threading import Event
from typing import Optional

from qmixsdk.qmixbus import DeviceError, PollingTimer
from qmixsdk.qmixpump import Pump
from sila2.server import MetadataDict, ObservableCommandInstance, SilaServer

from sila_cetoni.application.server_configuration import ServerConfiguration
from sila_cetoni.application.system import ApplicationSystem, requires_operational_system

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


class PumpDriveControlServiceImpl(PumpDriveControlServiceBase):
    __pump: Pump
    __is_initializing: bool
    __system: ApplicationSystem
    __config: ServerConfiguration
    __stop_event: Event

    __CALIBRATION_TIMEOUT = datetime.timedelta(seconds=60)

    def __init__(self, server: SilaServer, pump: Pump, executor: Executor):
        super().__init__(server)
        self.__pump = pump
        self.__is_initializing = False
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        def update_fault_state(stop_event: Event):
            new_fault_state = fault_state = self.__pump.is_in_fault_state()
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_fault_state = self.__pump.is_in_fault_state()
                if new_fault_state != fault_state:
                    fault_state = new_fault_state
                    self.update_FaultState(fault_state)
                time.sleep(0.1)

        def update_pump_drive_state(stop_event: Event):
            new_is_enabled = is_enabled = self.__pump.is_enabled() and self.__system.state.is_operational()
            new_is_initializing = is_initializing = self.__is_initializing
            while not stop_event.is_set():
                new_is_enabled = self.__pump.is_enabled() and self.__system.state.is_operational()
                new_is_initializing = self.__is_initializing
                if new_is_enabled != is_enabled or new_is_initializing != is_initializing:
                    is_enabled = new_is_enabled
                    is_initializing = new_is_initializing
                    self.update_PumpDriveState(
                        "Initializing" if is_initializing else "Enabled" if is_enabled else "Disabled"
                    )
                time.sleep(0.1)

        def update_drive_position_counter(stop_event: Event):
            new_pos_counter = pos_counter = (
                self.__pump.get_position_counter_value() if self.__system.state.is_operational() else 0
            )
            while not stop_event.is_set():
                new_pos_counter = (
                    self.__pump.get_position_counter_value() if self.__system.state.is_operational() else 0
                )
                if new_pos_counter != pos_counter:
                    pos_counter = new_pos_counter
                    self.update_DrivePositionCounter(pos_counter)
                time.sleep(0.1)

        executor.submit(update_fault_state, self.__stop_event)
        executor.submit(update_pump_drive_state, self.__stop_event)
        executor.submit(update_drive_position_counter, self.__stop_event)

    def start(self) -> None:
        self.__config = ServerConfiguration(self.parent_server.server_name, self.__system.device_config.name)
        if not self.__pump.is_position_sensing_initialized():
            self._restore_last_drive_position_counter()

        # initial property values
        self.update_FaultState(self.__pump.is_in_fault_state())
        self.update_PumpDriveState("Enabled" if self.__pump.is_enabled() else "Disabled")
        self.update_DrivePositionCounter(self.__pump.get_position_counter_value())

        super().start()

    def stop(self) -> None:
        super().stop()
        self.__stop_event.set()
        self.__config.write()

    def _restore_last_drive_position_counter(self):
        """
        Reads the last drive position counter from the server's config file.
        """
        drive_pos_counter = self.__config.pump_drive_position_counter
        if drive_pos_counter is not None:
            logger.debug(f"Restoring drive position counter: {drive_pos_counter}")
            self.__pump.restore_position_counter_value(drive_pos_counter)
        else:
            logger.warning(
                f"Could not read drive position counter for {self.__pump.get_pump_name()} from config file. "
                "Reference move needed!"
            )

    def update_DrivePositionCounter(self, DrivePositionCounter: int, queue: Optional[Queue[int]] = None):
        self.__config.pump_drive_position_counter = DrivePositionCounter
        return super().update_DrivePositionCounter(DrivePositionCounter, queue)

    @requires_operational_system(PumpDriveControlServiceFeature)
    def EnablePumpDrive(self, *, metadata: MetadataDict) -> EnablePumpDrive_Responses:
        self.__pump.clear_fault()
        self.__pump.enable(True)
        self.update_PumpDriveState("Enabled" if self.__pump.is_enabled() else "Disabled")

    @requires_operational_system(PumpDriveControlServiceFeature)
    def DisablePumpDrive(self, *, metadata: MetadataDict) -> DisablePumpDrive_Responses:
        self.__pump.enable(False)
        self.update_PumpDriveState("Enabled" if self.__pump.is_enabled() else "Disabled")

    @requires_operational_system(PumpDriveControlServiceFeature)
    def RestoreDrivePositionCounter(
        self, DrivePositionCounterValue: int, *, metadata: MetadataDict
    ) -> RestoreDrivePositionCounter_Responses:
        try:
            self.__pump.restore_position_counter_value(DrivePositionCounterValue)
        except DeviceError as err:
            if err.errorcode == -0x00CA:  # -ERR_DEVNOSUPP
                raise NotSupported(str(err))
            raise

    @requires_operational_system(PumpDriveControlServiceFeature)
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
