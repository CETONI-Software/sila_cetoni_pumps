from __future__ import annotations

import math
import time
from concurrent.futures import Executor
from threading import Event

from qmixsdk.qmixpump import Pump
from sila2.server import MetadataDict, SilaServer

from sila_cetoni.application.system import ApplicationSystem, requires_operational_system

from ..generated.forcemonitoringservice import (
    ClearForceSafetyStop_Responses,
    DisableForceMonitoring_Responses,
    EnableForceMonitoring_Responses,
    Force,
    ForceMonitoringServiceBase,
    ForceMonitoringServiceFeature,
    SetForceLimit_Responses,
)


class ForceMonitoringServiceImpl(ForceMonitoringServiceBase):
    __pump: Pump
    __system: ApplicationSystem
    __stop_event: Event

    def __init__(self, server: SilaServer, pump: Pump, executor: Executor):
        super().__init__(server)
        self.__pump = pump
        self.__system = ApplicationSystem()
        self.__stop_event = Event()

        def update_force_limit(stop_event: Event):
            new_force_limit = force_limit = self.__pump.get_force_limit()
            while not stop_event.is_set():
                new_force_limit = self.__pump.get_force_limit()
                if not math.isclose(new_force_limit, force_limit):
                    force_limit = new_force_limit
                    self.update_ForceLimit(force_limit)
                time.sleep(0.1)

        def update_force_monitoring_enabled(stop_event: Event):
            new_is_enabled = is_enabled = self.__pump.is_force_monitoring_enabled()
            while not stop_event.is_set():
                new_is_enabled = self.__pump.is_force_monitoring_enabled()
                if not math.isclose(new_is_enabled, is_enabled):
                    is_enabled = new_is_enabled
                    self.update_ForceMonitoringEnabled(is_enabled)
                time.sleep(0.1)

        def update_force_safety_stop_active(stop_event: Event):
            new_is_active = is_active = self.__pump.is_force_safety_stop_active()
            while not stop_event.is_set():
                new_is_active = self.__pump.is_force_safety_stop_active()
                if not math.isclose(new_is_active, is_active):
                    is_active = new_is_active
                    self.update_ForceSafetyStopActive(is_active)
                time.sleep(0.1)

        def update_force_sensor_value(stop_event: Event):
            new_force = force = self.__pump.read_force_sensor()
            while not stop_event.is_set():
                new_force = self.__pump.read_force_sensor()
                if not math.isclose(new_force, force, abs_tol=1.0e-3):
                    force = new_force
                    self.update_ForceSensorValue(force)
                time.sleep(0.1)

        def update_max_device_force(stop_event: Event):
            new_max_force = max_force = self.__pump.get_max_device_force()
            while not stop_event.is_set():
                new_max_force = self.__pump.get_max_device_force()
                if not math.isclose(new_max_force, max_force):
                    max_force = new_max_force
                    self.update_MaxDeviceForce(max_force)
                time.sleep(0.1)

        # initial values
        self.update_ForceLimit(self.__pump.get_force_limit())
        self.update_ForceMonitoringEnabled(self.__pump.is_force_monitoring_enabled())
        self.update_ForceSafetyStopActive(self.__pump.is_force_safety_stop_active())
        self.update_ForceSensorValue(self.__pump.read_force_sensor())
        self.update_MaxDeviceForce(self.__pump.get_max_device_force())

        executor.submit(update_force_limit, self.__stop_event)
        executor.submit(update_force_monitoring_enabled, self.__stop_event)
        executor.submit(update_force_safety_stop_active, self.__stop_event)
        executor.submit(update_force_sensor_value, self.__stop_event)
        executor.submit(update_max_device_force, self.__stop_event)

    @requires_operational_system(ForceMonitoringServiceFeature)
    def ClearForceSafetyStop(self, *, metadata: MetadataDict) -> ClearForceSafetyStop_Responses:
        self.__pump.clear_force_safety_stop()

    @requires_operational_system(ForceMonitoringServiceFeature)
    def EnableForceMonitoring(self, *, metadata: MetadataDict) -> EnableForceMonitoring_Responses:
        self.__pump.enable_force_monitoring(True)

    @requires_operational_system(ForceMonitoringServiceFeature)
    def DisableForceMonitoring(self, *, metadata: MetadataDict) -> DisableForceMonitoring_Responses:
        self.__pump.enable_force_monitoring(False)

    @requires_operational_system(ForceMonitoringServiceFeature)
    def SetForceLimit(self, ForceLimit: Force, *, metadata: MetadataDict) -> SetForceLimit_Responses:
        self.__pump.write_force_limit(ForceLimit)

    def stop(self) -> None:
        super().stop()
        self.__stop_event.set()
