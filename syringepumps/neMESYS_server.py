#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: SiLA2_python

*neMESYS*

:details: neMESYS:
    This is a sample service for controlling neMESYS syringe pumps via SiLA2

:file:    neMESYS_server.py
:authors: Florian Meinicke

:date: (creation)          2019-07-16T11:11:31.321083
:date: (last modification) 2020-05-07

.. note:: Code generated by SiLA2CodeGenerator 0.2.0

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.1.0"

import os
import argparse
from configparser import ConfigParser
from typing import Union, Tuple
import logging
try:
    import coloredlogs
except ModuleNotFoundError:
    print("Cannot find coloredlogs! Please install coloredlogs, if you'd like to have nicer logging output:")
    print("`pip install coloredlogs`")


# import qmixsdk
from qmixsdk import qmixbus, qmixpump, qmixvalve

# Import our server base class
from ...io.QmixIO_server import QmixIOServer

# Import gRPC libraries of features
from impl.de.cetoni.pumps.syringepumps.PumpDriveControlService.gRPC import PumpDriveControlService_pb2
from impl.de.cetoni.pumps.syringepumps.PumpDriveControlService.gRPC import PumpDriveControlService_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.pumps.syringepumps.PumpDriveControlService.PumpDriveControlService_default_arguments import default_dict as PumpDriveControlService_default_dict
from impl.de.cetoni.pumps.syringepumps.PumpUnitController.gRPC import PumpUnitController_pb2
from impl.de.cetoni.pumps.syringepumps.PumpUnitController.gRPC import PumpUnitController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.pumps.syringepumps.PumpUnitController.PumpUnitController_default_arguments import default_dict as PumpUnitController_default_dict
from impl.de.cetoni.pumps.syringepumps.PumpFluidDosingService.gRPC import PumpFluidDosingService_pb2
from impl.de.cetoni.pumps.syringepumps.PumpFluidDosingService.gRPC import PumpFluidDosingService_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.pumps.syringepumps.PumpFluidDosingService.PumpFluidDosingService_default_arguments import default_dict as PumpFluidDosingService_default_dict
from impl.de.cetoni.pumps.syringepumps.SyringeConfigurationController.gRPC import SyringeConfigurationController_pb2
from impl.de.cetoni.pumps.syringepumps.SyringeConfigurationController.gRPC import SyringeConfigurationController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.pumps.syringepumps.SyringeConfigurationController.SyringeConfigurationController_default_arguments import default_dict as SyringeConfigurationController_default_dict
from impl.de.cetoni.valves.ValvePositionController.gRPC import ValvePositionController_pb2
from impl.de.cetoni.valves.ValvePositionController.gRPC import ValvePositionController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.valves.ValvePositionController.ValvePositionController_default_arguments import default_dict as ValvePositionController_default_dict
from impl.de.cetoni.core.ShutdownController.gRPC import ShutdownController_pb2
from impl.de.cetoni.core.ShutdownController.gRPC import ShutdownController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.core.ShutdownController.ShutdownController_default_arguments import default_dict as ShutdownController_default_dict

# Import the servicer modules for each feature
from impl.de.cetoni.pumps.syringepumps.PumpDriveControlService.PumpDriveControlService_servicer import PumpDriveControlService
from impl.de.cetoni.pumps.syringepumps.PumpUnitController.PumpUnitController_servicer import PumpUnitController
from impl.de.cetoni.pumps.syringepumps.PumpFluidDosingService.PumpFluidDosingService_servicer import PumpFluidDosingService
from impl.de.cetoni.pumps.syringepumps.SyringeConfigurationController.SyringeConfigurationController_servicer import SyringeConfigurationController
from impl.de.cetoni.valves.ValvePositionController.ValvePositionController_servicer import ValvePositionController
from impl.de.cetoni.core.ShutdownController.ShutdownController_servicer import ShutdownController

class neMESYSServer(QmixIOServer):
    """
    This is a sample service for controlling neMESYS syringe pumps via SiLA2
    """

    def __init__(
        self,
        cmd_args,
        qmix_pump: Union[qmixpump.Pump, qmixpump.ContiFlowPump],
        valve: qmixvalve.Valve = None,
        io_channels = [],
        simulation_mode: bool = True):
        """
        Class initialiser

            :param cmd_args: Arguments that were given on the command line
            :param qmix_pump: The qmixpump.Pump object that this server shall use
            :param valve: (optional) The valve of this pump
            :param io_channels: (optional) I/O channels of the pump
            :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode
        """
        super().__init__(cmd_args, io_channels, simulation_mode=simulation_mode)

        data_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..',
                                                 'features', 'de', 'cetoni', 'pumps', 'syringepumps'))

        # registering common pump features
        #  Register de.cetoni.pumps.syringepumps.PumpDriveControlService
        self.PumpDriveControlService_servicer = PumpDriveControlService(
            pump=qmix_pump,
            sila2_conf=self.sila2_config,
            simulation_mode=simulation_mode)
        PumpDriveControlService_pb2_grpc.add_PumpDriveControlServiceServicer_to_server(
            self.PumpDriveControlService_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='PumpDriveControlService',
                         servicer=self.PumpDriveControlService_servicer,
                         data_path=data_path)
        #  Register de.cetoni.pumps.syringepumps.PumpUnitController
        self.PumpUnitController_servicer = PumpUnitController(
            pump=qmix_pump,
            simulation_mode=simulation_mode)
        PumpUnitController_pb2_grpc.add_PumpUnitControllerServicer_to_server(
            self.PumpUnitController_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='PumpUnitController',
                         servicer=self.PumpUnitController_servicer,
                         data_path=data_path)

        if not isinstance(qmix_pump, qmixpump.ContiFlowPump):
            # registering features not for contiflow pumps
            #  Register de.cetoni.pumps.syringepumps.SyringeConfigurationController
            self.SyringeConfigurationController_servicer = SyringeConfigurationController(
                pump=qmix_pump,
                simulation_mode=simulation_mode)
            SyringeConfigurationController_pb2_grpc.add_SyringeConfigurationControllerServicer_to_server(
                self.SyringeConfigurationController_servicer,
                self.grpc_server
            )
            self.add_feature(feature_id='SyringeConfigurationController',
                             servicer=self.SyringeConfigurationController_servicer,
                             data_path=data_path)
            #  Register de.cetoni.pumps.syringepumps.PumpFluidDosingService
            self.PumpFluidDosingService_servicer = PumpFluidDosingService(
                pump=qmix_pump,
                simulation_mode=simulation_mode)
            PumpFluidDosingService_pb2_grpc.add_PumpFluidDosingServiceServicer_to_server(
                self.PumpFluidDosingService_servicer,
                self.grpc_server
            )
            self.add_feature(feature_id='PumpFluidDosingService',
                             servicer=self.PumpFluidDosingService_servicer,
                             data_path=data_path)
            if valve is not None:
                #  Register de.cetoni.valves.ValvePositionController
                self.ValvePositionController_servicer = ValvePositionController(
                    valve=valve,
                    simulation_mode=simulation_mode)
                ValvePositionController_pb2_grpc.add_ValvePositionControllerServicer_to_server(
                    self.ValvePositionController_servicer,
                    self.grpc_server
                )
                self.add_feature(feature_id='ValvePositionController',
                                servicer=self.ValvePositionController_servicer,
                                data_path=data_path.replace(os.path.join('pumps', 'syringepumps'), 'valves'))

        #  Register de.cetoni.core.ShutdownController
        self.ShutdownController_servicer = ShutdownController(
            device=qmix_pump,
            server_name=self.server_name,
            sila2_conf=self.sila2_config,
            simulation_mode=simulation_mode
        )
        ShutdownController_pb2_grpc.add_ShutdownControllerServicer_to_server(
            self.ShutdownController_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='ShutdownController',
                            servicer=self.ShutdownController_servicer,
                            data_path=data_path.replace(os.path.join('pumps', 'syringepumps'), 'core'))

        self.simulation_mode = simulation_mode


    def switchToSimMode(self):
        """Switch to simulation mode of the server"""

        # perform implementation specific switch operations
        self.PumpDriveControlService_servicer.switch_to_simulation_mode()
        self.PumpUnitController_servicer.switch_to_simulation_mode()
        self.PumpFluidDosingService_servicer.switch_to_simulation_mode()
        self.SyringeConfigurationController_servicer.switch_to_simulation_mode()
        self.ValvePositionController_servicer.switch_to_simulation_mode()
        self.ShutdownController_servicer.switch_to_simulation_mode()

        self.simulation_mode = True

    def switchToRealMode(self):
        """Switch to real mode"""

        # perform implementation specific switch operations
        self.PumpDriveControlService_servicer.switch_to_real_mode()
        self.PumpUnitController_servicer.switch_to_real_mode()
        self.PumpFluidDosingService_servicer.switch_to_real_mode()
        self.SyringeConfigurationController_servicer.switch_to_real_mode()
        self.ValvePositionController_servicer.switch_to_real_mode()
        self.ShutdownController_servicer.switch_to_real_mode()

        self.simulation_mode = False

def connect_to_bus_and_enable_pump(config_path: str) -> Tuple[qmixbus.Bus, qmixpump.Pump]:
    """
        Loads a valid Qmix configuration, connects to the bus,
        retrieves the pump and enables it.

        :param config_path: Path to a valid Qmix device configuration
        :type config_path: str
        :return: A tuple containing the opened and started bus as well as the enabled pump.
        :rtype: tuple
    """
    logging.debug("Opening bus")
    bus = qmixbus.Bus()
    try:
        bus.open(config_path, 0)
    except qmixbus.DeviceError as err:
        logging.error("could not open the bus communication: %s", err)

    logging.debug("Looking up pump...")
    if qmixpump.Pump.get_no_of_pumps() > 1:
        logging.info("Found more than one pump but this SiLA server will only use the first pump. Use the SiLA_neMESYS.py script if you want to control multiple pumps via SiLA 2.")

    pump = qmixpump.Pump()
    pump.lookup_by_device_index(0)

    bus.start()

    if pump.is_in_fault_state():
        pump.clear_fault()
    if not pump.is_enabled():
        pump.enable(True)

    return (bus, pump)


def parse_command_line():
    """
    Just looking for commandline arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 service: neMESYS")

    # Simple arguments for the server identification
    parser.add_argument('-p', '--port', action='store',
                        default="50053", help='start SiLA server at [port]')
    parser.add_argument('-s', '--server-name', action='store',
                        default="neMESYS", help='start SiLA server with [server-name]')
    parser.add_argument('-t', '--server-type', action='store',
                        default="Unknown Type", help='start SiLA server with [server-type]')
    parser.add_argument('-d', '--description', action='store',
                        default="This is a sample service for controlling neMESYS syringe pumps via SiLA2", help='SiLA server description')

    # Encryption
    parser.add_argument('-X', '--encryption', action='store', default=None,
                        help='The name of the private key and certificate file (without extension).')
    parser.add_argument('--encryption-key', action='store', default=None,
                        help='The name of the encryption key (*with* extension). Can be used if key and certificate '
                             'vary or non-standard file extensions are used.')
    parser.add_argument('--encryption-cert', action='store', default=None,
                        help='The name of the encryption certificate (*with* extension). Can be used if key and '
                             'certificate vary or non-standard file extensions are used.')

    # Qmix configuration
    parser.add_argument('config_path', metavar='configuration_path', type=str,
                        help="""a path to a valid Qmix configuration folder
                             (If you don't have a configuration yet,
                             create one with the QmixElements software first.)""")

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parsed_args = parser.parse_args()

    # validate/update some settings
    #   encryption
    if parsed_args.encryption is not None:
        # only overwrite the separate keys if not given manually
        if parsed_args.encryption_key is None:
            parsed_args.encryption_key = parsed_args.encryption + '.key'
        if parsed_args.encryption_cert is None:
            parsed_args.encryption_cert = parsed_args.encryption + '.cert'

    return parsed_args


if __name__ == '__main__':
    logging_level = logging.INFO # or use logging.ERROR for less output
    try:
        coloredlogs.install(fmt='%(asctime)s %(levelname)s| %(module)s.%(funcName)s: %(message)s',
                            level=logging_level)
    except NameError:
        logging.basicConfig(format='%(levelname)s| %(module)s.%(funcName)s: %(message)s', level=logging_level)

    args = parse_command_line()

    # generate SiLA2Server
    bus, pump = connect_to_bus_and_enable_pump(args.config_path)
    sila_server = neMESYSServer(
        cmd_args=args,
        qmix_pump=pump,
        simulation_mode=False
    )
    # starting and running the gRPC/SiLA2 server
    sila_server.run()
    print()
