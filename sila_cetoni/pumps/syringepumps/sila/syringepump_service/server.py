from __future__ import annotations

from typing import List, Optional, Union
from uuid import UUID

from qmixsdk.qmixpump import ContiFlowPump, Pump
from qmixsdk.qmixvalve import Valve

from sila_cetoni.core.device_drivers.abc import BatteryInterface
from sila_cetoni.io.sila.io_service.server import Server as IOServer
from sila_cetoni.valves.sila.valve_service.feature_implementations.valvepositioncontroller_impl import (
    ValvePositionControllerImpl,
)
from sila_cetoni.valves.sila.valve_service.generated.valvepositioncontroller import ValvePositionControllerFeature

from .feature_implementations.forcemonitoringservice_impl import ForceMonitoringServiceImpl
from .feature_implementations.pumpdrivecontrolservice_impl import PumpDriveControlServiceImpl
from .feature_implementations.pumpfluiddosingservice_impl import PumpFluidDosingServiceImpl
from .feature_implementations.pumpunitcontroller_impl import PumpUnitControllerImpl
from .feature_implementations.syringeconfigurationcontroller_impl import SyringeConfigurationControllerImpl
from .generated.forcemonitoringservice import ForceMonitoringServiceFeature
from .generated.pumpdrivecontrolservice import PumpDriveControlServiceFeature
from .generated.pumpfluiddosingservice import PumpFluidDosingServiceFeature
from .generated.pumpunitcontroller import PumpUnitControllerFeature
from .generated.syringeconfigurationcontroller import SyringeConfigurationControllerFeature

__version__ = "1.7.1"


class Server(IOServer):
    def __init__(
        self,
        pump: Union[Pump, ContiFlowPump],
        valve: Optional[Valve] = None,
        io_channels: List = [],
        battery: Optional[BatteryInterface] = None,
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None,
    ):
        super().__init__(
            io_channels,
            battery,
            server_name=server_name or "Syringe Pump Service",
            server_type=server_type or "TestServer",
            server_description=server_description or "The SiLA 2 driver for CETONI syringe pumps",
            server_version=server_version or __version__,
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid,
        )

        # common features
        self.pumpdrivecontrolservice = PumpDriveControlServiceImpl(self, pump, self.child_task_executor)
        self.pumpunitcontroller = PumpUnitControllerImpl(self, pump, self.child_task_executor)
        self.set_feature_implementation(PumpDriveControlServiceFeature, self.pumpdrivecontrolservice)
        self.set_feature_implementation(PumpUnitControllerFeature, self.pumpunitcontroller)

        if not isinstance(pump, ContiFlowPump):
            # features for real syringe pumps only
            self.syringeconfigurationcontroller = SyringeConfigurationControllerImpl(
                self, pump, self.child_task_executor
            )
            self.set_feature_implementation(SyringeConfigurationControllerFeature, self.syringeconfigurationcontroller)

            try:
                if pump.has_force_monitoring():
                    self.forcemonitoringservice = ForceMonitoringServiceImpl(self, pump, self.child_task_executor)
                    self.set_feature_implementation(ForceMonitoringServiceFeature, self.forcemonitoringservice)
            except AttributeError:
                pass

            self.pumpfluiddosingservice = PumpFluidDosingServiceImpl(self, pump, self.child_task_executor)
            self.set_feature_implementation(PumpFluidDosingServiceFeature, self.pumpfluiddosingservice)

            if valve:
                self.valvepositioncontroller = ValvePositionControllerImpl(
                    self, valve=valve, executor=self.child_task_executor
                )
                self.set_feature_implementation(ValvePositionControllerFeature, self.valvepositioncontroller)

        # TODO shutdown controller
