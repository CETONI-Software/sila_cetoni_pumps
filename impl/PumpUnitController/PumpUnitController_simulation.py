"""
________________________________________________________________________

:PROJECT: SiLA2_python

*Pump Unit Controller*

:details: PumpUnitController:
    Allows to control the currently used units for passing and retrieving flow rates and volumes to and from a pump.

:file:    PumpUnitController_simulation.py
:authors: Florian Meinicke

:date: (creation)          2019-07-16T11:11:31.289569
:date: (last modification) 2019-10-05T11:53:30.820262

.. note:: Code generated by SiLA2CodeGenerator 0.2.0

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.0.1"

# import general packages
import logging
import time         # used for observables
import uuid         # used for observables
import grpc         # used for type hinting only

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

# import gRPC modules for this feature
from .gRPC import PumpUnitController_pb2 as PumpUnitController_pb2
# from .gRPC import PumpUnitController_pb2_grpc as PumpUnitController_pb2_grpc

# import default arguments
from .PumpUnitController_default_arguments import default_dict


# noinspection PyPep8Naming,PyUnusedLocal
class PumpUnitControllerSimulation:
    """
    Implementation of the *Pump Unit Controller* in *Simulation* mode
        This is a sample service for controlling neMESYS syringe pumps via SiLA2
    """

    def __init__(self):
        """Class initialiser"""

        logging.debug('Started server in mode: {mode}'.format(mode='Simulation'))

    def _get_command_state(self, command_uuid: str) -> silaFW_pb2.ExecutionInfo:
        """
        Method to fill an ExecutionInfo message from the SiLA server for observable commands

        :param command_uuid: The uuid of the command for which to return the current state

        :return: An execution info object with the current command state
        """

        #: Enumeration of silaFW_pb2.ExecutionInfo.CommandStatus
        command_status = silaFW_pb2.ExecutionInfo.CommandStatus.waiting
        #: Real silaFW_pb2.Real(0...1)
        command_progress = None
        #: Duration silaFW_pb2.Duration(seconds=<seconds>, nanos=<nanos>)
        command_estimated_remaining = None
        #: Duration silaFW_pb2.Duration(seconds=<seconds>, nanos=<nanos>)
        command_lifetime_of_execution = None

        # TODO: check the state of the command with the given uuid and return the correct information

        # just return a default in this example
        return silaFW_pb2.ExecutionInfo(
            commandStatus=command_status,
            progressInfo=(
                command_progress if command_progress is not None else None
            ),
            estimatedRemainingTime=(
                command_estimated_remaining if command_estimated_remaining is not None else None
            ),
            updatedLifetimeOfExecution=(
                command_lifetime_of_execution if command_lifetime_of_execution is not None else None
            )
        )

    def SetFlowUnit(self, request, context: grpc.ServicerContext) \
            -> PumpUnitController_pb2.SetFlowUnit_Responses:
        """
        Executes the unobservable command "Set Flow Unit"
            Sets the flow unit for the pump. The flow unit defines the unit to be used for all flow values passed to or retrieved from the pump.
    
        :param request: gRPC request containing the parameters passed:
            request.FlowUnit (FlowUnit): The flow unit to set. It has to something like "ml/s" or "µl/s", for instance.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
    
        # initialise the return value
        return_value = None
    
        # TODO:
        #   Add implementation of Simulation for command SetFlowUnit here and write the resulting response
        #   in return_value
    
        # fallback to default
        if return_value is None:
            return_value = PumpUnitController_pb2.SetFlowUnit_Responses(
                **default_dict['SetFlowUnit_Responses']
            )
    
        return return_value
    
    
    def SetVolumeUnit(self, request, context: grpc.ServicerContext) \
            -> PumpUnitController_pb2.SetVolumeUnit_Responses:
        """
        Executes the unobservable command "Set Volume Unit"
            Sets the default volume unit. The volume unit defines the unit to be used for all volume values passed to or retrieved from the pump.
    
        :param request: gRPC request containing the parameters passed:
            request.VolumeUnit (Volume Unit): The volume unit to set. It has to be something like "ml" or "µl", for instance.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
    
        # initialise the return value
        return_value = None
    
        # TODO:
        #   Add implementation of Simulation for command SetVolumeUnit here and write the resulting response
        #   in return_value
    
        # fallback to default
        if return_value is None:
            return_value = PumpUnitController_pb2.SetVolumeUnit_Responses(
                **default_dict['SetVolumeUnit_Responses']
            )
    
        return return_value
    

    def Subscribe_FlowUnit(self, request, context: grpc.ServicerContext) \
            -> PumpUnitController_pb2.Subscribe_FlowUnit_Responses:
        """
        Requests the observable property Flow Unit
            The currently used flow unit.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.FlowUnit (Flow Unit): The currently used flow unit.
        """
    
        # initialise the return value
        return_value: PumpUnitController_pb2.Subscribe_FlowUnit_Responses = None
    
        # we could use a timeout here if we wanted
        while True:
            # TODO:
            #   Add implementation of Simulation for property FlowUnit here and write the resulting
            #   response in return_value
    
            # create the default value
            if return_value is None:
                return_value = PumpUnitController_pb2.Subscribe_FlowUnit_Responses(
                    **default_dict['Subscribe_FlowUnit_Responses']
                )
    
    
            yield return_value
    
    
    def Subscribe_VolumeUnit(self, request, context: grpc.ServicerContext) \
            -> PumpUnitController_pb2.Subscribe_VolumeUnit_Responses:
        """
        Requests the observable property Volume Unit
            The currently used volume unit.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.VolumeUnit (Volume Unit): The currently used volume unit.
        """
    
        # initialise the return value
        return_value: PumpUnitController_pb2.Subscribe_VolumeUnit_Responses = None
    
        # we could use a timeout here if we wanted
        while True:
            # TODO:
            #   Add implementation of Simulation for property VolumeUnit here and write the resulting
            #   response in return_value
    
            # create the default value
            if return_value is None:
                return_value = PumpUnitController_pb2.Subscribe_VolumeUnit_Responses(
                    **default_dict['Subscribe_VolumeUnit_Responses']
                )
    
    
            yield return_value
    
