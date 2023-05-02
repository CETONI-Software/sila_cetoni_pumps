from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Dict, List, Optional, Union, overload

if TYPE_CHECKING:
    from sila_cetoni.application.application_configuration import ApplicationConfiguration
    from sila_cetoni.application.cetoni_device_configuration import CetoniDeviceConfiguration

from qmixsdk import qmixbus, qmixpump

from sila_cetoni.application.device import CetoniDevice
from sila_cetoni.utils import get_version

from .contiflowpumps.sila.contiflowpump_service.server import Server as ContiflowPumpServer
from .syringepumps.sila.syringepump_service.server import Server as SyringePumpServer

__version__ = get_version(__name__)

logger = logging.getLogger(__name__)


class CetoniPumpDevice(CetoniDevice[qmixpump.Pump]):
    """
    Simple wrapper around `qmixpump.Pump` with additional information from the `CetoniDevice` class
    """

    _is_contiflow_pump: bool
    _is_peristaltic_pump: bool

    def __init__(self, name: str, handle: qmixpump.Pump) -> None:
        super().__init__(name, "pumps", handle)
        self._is_contiflow_pump = isinstance(handle, qmixpump.ContiFlowPump)
        self._is_peristaltic_pump = False

    @property
    def is_contiflow_pump(self) -> bool:
        return self._is_contiflow_pump

    @property
    def is_peristaltic_pump(self) -> bool:
        return self._is_peristaltic_pump

    @is_peristaltic_pump.setter
    def is_peristaltic_pump(self, is_peristaltic_pump):
        self._is_peristaltic_pump = is_peristaltic_pump

    def set_operational(self):
        ERR_DS402_DRV_ENABLE_FAULT_STATE = 0x0644

        super().set_operational()
        self._device_handle.clear_fault()
        time.sleep(0.1)  # wait for pump to clear fault
        self._device_handle.enable(False)
        while not self._device_handle.is_enabled():
            try:
                self._device_handle.enable(True)
            except qmixbus.DeviceError as err:
                if err.errorcode != -ERR_DS402_DRV_ENABLE_FAULT_STATE:
                    raise


def parse_devices(json_devices: Optional[Dict[str, Dict]]) -> List[CetoniPumpDevice]:
    """
    Parses the given JSON configuration `json_devices` and creates the necessary `CetoniPumpDevice`s

    Parameters
    ----------
    json_devices: Dict[str, Dict] (optional)
        The `"devices"` section of the JSON configuration file as a dictionary (key is the device name, the value is a
        dictionary with the configuration parameters for the device, i.e. `"type"`, `"manufacturer"`, ...)

    Returns
    -------
    List[CetoniPumpDevice]
        A list with all `CetoniPumpDevice`s as defined in the JSON config
    """
    # CETONI devices are not defined directly in the JSON config
    return []


@overload
def create_devices(config: ApplicationConfiguration, scan: bool = False) -> None:
    """
    Looks up all controller devices from the current configuration and tries to auto-detect more devices if `scan` is
    `True`

    Parameters
    ----------
    config: ApplicationConfiguration
        The application configuration containing all devices for which SiLA Server and thus device driver instances
        shall be created
    scan: bool (default: False)
        Whether to scan for more devices than the ones defined in `config`
    """
    ...


@overload
def create_devices(config: CetoniDeviceConfiguration) -> List[CetoniPumpDevice]:
    """
    Looks up all CETONI devices from the given configuration `config` and creates the necessary `CetoniPumpDevice`s for
    them

    Parameters
    ----------
    config: CetoniDeviceConfiguration
        The CETONI device configuration

    Returns
    -------
    List[CetoniPumpDevice]
        A list with all `Device`s from the device configuration
    """
    ...


def create_devices(config: Union[ApplicationConfiguration, CetoniDeviceConfiguration], *args, **kwargs):
    from sila_cetoni.application.application_configuration import ApplicationConfiguration
    from sila_cetoni.application.cetoni_device_configuration import CetoniDeviceConfiguration

    if isinstance(config, ApplicationConfiguration):
        logger.info(
            f"Package {__name__!r} currently only supports CETONI devices. Parameter 'config' must be of type "
            f"'CetoniDeviceConfiguration'!"
        )
        return
    if isinstance(config, CetoniDeviceConfiguration):
        return create_devices_cetoni(config)
    raise ValueError(
        f"Parameter 'config' must be of type 'ApplicationConfiguration' or 'CetoniDeviceConfiguration', not"
        f"{type(config)!r}!"
    )


def create_devices_cetoni(config: CetoniDeviceConfiguration) -> List[CetoniPumpDevice]:
    """
    Implementation of `create_devices` for devices from the CETONI device config

    See `create_devices` for an explanation of the parameters and return value
    """

    pump_count = qmixpump.Pump.get_no_of_pumps()
    logger.debug(f"Number of pumps: {pump_count}")

    devices: List[CetoniPumpDevice] = []
    for i in range(pump_count):
        pump = qmixpump.Pump()
        pump.lookup_by_device_index(i)
        pump_name = pump.get_device_name()
        logger.debug(f"Found pump {i} named {pump_name}")
        try:
            pump.get_device_property(qmixpump.ContiFlowProperty.SWITCHING_MODE)
            pump = qmixpump.ContiFlowPump(pump.handle)
            logger.debug(f"Pump {pump_name} is contiflow pump")
        except qmixbus.DeviceError:
            pass
        devices.append(CetoniPumpDevice(pump_name, pump))
    return devices


def create_server(device: CetoniPumpDevice, **server_args) -> Union[SyringePumpServer, ContiflowPumpServer]:
    """
    Creates the SiLA Server for the given `device`

    Parameters
    ----------
    device: Device
        The device for which to create a SiLA Server
    **server_args
        Additional arguments like server name, server UUID to pass to the server's `__init__` function
    """
    logger.info(f"Creating server for {device}")
    if device.is_contiflow_pump:
        return ContiflowPumpServer(pump=device.device_handle, **server_args)
    elif device.is_peristaltic_pump:
        # server = PeristalticPumpServer(pump=device.device_handle, **common_args)
        logger.info(f"No support for peristaltic pumps yet! Skipping creation of SiLA Server for {device.name}.")
    else:
        return SyringePumpServer(
            pump=device.device_handle,
            valve=device.valves[0] if len(device.valves) > 0 else None,
            io_channels=device.io_channels,
            **server_args,
        )
