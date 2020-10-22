"""
________________________________________________________________________

:PROJECT: SiLA2_python

*Continuous Flow Configuration Service*

:details: ContinuousFlowConfigurationService:
    Allows to configure the parameters of a continuous flow pump.

:file:    ContinuousFlowConfigurationService_simulation.py
:authors: Florian Meinicke

:date: (creation)          2020-10-22T07:15:49.899157
:date: (last modification) 2020-10-22T07:15:49.899157

.. note:: Code generated by sila2codegenerator 0.3.2.dev

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.1.0"

# import general packages
import logging
import time         # used for observables
import uuid         # used for observables
import grpc         # used for type hinting only

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

# import gRPC modules for this feature
from .gRPC import ContinuousFlowConfigurationService_pb2 as ContinuousFlowConfigurationService_pb2
# from .gRPC import ContinuousFlowConfigurationService_pb2_grpc as ContinuousFlowConfigurationService_pb2_grpc

# import default arguments
from .ContinuousFlowConfigurationService_default_arguments import default_dict


# noinspection PyPep8Naming,PyUnusedLocal
class ContinuousFlowConfigurationServiceSimulation:
    """
    Implementation of the *Continuous Flow Configuration Service* in *Simulation* mode
        Allows to control a continuous flow pumps that is made up of two syringe pumps
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

    def SetSwitchingMode(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowConfigurationService_pb2.SetSwitchingMode_Responses:
        """
        Executes the unobservable command "Set Switching Mode"
            Sets the switching mode for syringe pump switchover if one syringe pump runs empty.
    
        :param request: gRPC request containing the parameters passed:
            request.SwtichingMode (Switching Mode): The new switching mode to set
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
    
        # initialise the return value
        return_value = None
    
        # TODO:
        #   Add implementation of Simulation for command SetSwitchingMode here and write the resulting response
        #   in return_value
    
        # fallback to default
        if return_value is None:
            return_value = ContinuousFlowConfigurationService_pb2.SetSwitchingMode_Responses(
                **default_dict['SetSwitchingMode_Responses']
            )
    
        return return_value
    
    
    def SetRefillFlowRate(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowConfigurationService_pb2.SetRefillFlowRate_Responses:
        """
        Executes the unobservable command "Set Refill Flow Rate"
            Set the refill flow rate for the continuous flow pump. The refill flow speed limits the maximum flow that is possible with a contiflow pump.
    
        :param request: gRPC request containing the parameters passed:
            request.RefillFlowRate (Refill Flow Rate): The refill flow rate to set
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
    
        # initialise the return value
        return_value = None
    
        # TODO:
        #   Add implementation of Simulation for command SetRefillFlowRate here and write the resulting response
        #   in return_value
    
        # fallback to default
        if return_value is None:
            return_value = ContinuousFlowConfigurationService_pb2.SetRefillFlowRate_Responses(
                **default_dict['SetRefillFlowRate_Responses']
            )
    
        return return_value
    
    
    def SetCrossFlowDuration(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowConfigurationService_pb2.SetCrossFlowDuration_Responses:
        """
        Executes the unobservable command "Set Cross Flow Duration"
            Set the cross flow duration for the continuous flow pump. The cross flow duration is the time the pump running empty decelerates while the filled pump accelerates.
    
        :param request: gRPC request containing the parameters passed:
            request.CrossFlowDuration (Cross Flow Duration): The cross flow duration to set
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
    
        # initialise the return value
        return_value = None
    
        # TODO:
        #   Add implementation of Simulation for command SetCrossFlowDuration here and write the resulting response
        #   in return_value
    
        # fallback to default
        if return_value is None:
            return_value = ContinuousFlowConfigurationService_pb2.SetCrossFlowDuration_Responses(
                **default_dict['SetCrossFlowDuration_Responses']
            )
    
        return return_value
    
    
    def SetOverlapDuration(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowConfigurationService_pb2.SetOverlapDuration_Responses:
        """
        Executes the unobservable command "Set Overlap Duration"
            Set the overlap duration for the continuous flow pump. The overlap duration is a time the refilled pump will start earlier than the empty pump stops. You can use this time to ensure that the system is already pressurized when switching over.
    
        :param request: gRPC request containing the parameters passed:
            request.OverlapDuration (Overlap Duration): The overlap duration to set
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
    
        # initialise the return value
        return_value = None
    
        # TODO:
        #   Add implementation of Simulation for command SetOverlapDuration here and write the resulting response
        #   in return_value
    
        # fallback to default
        if return_value is None:
            return_value = ContinuousFlowConfigurationService_pb2.SetOverlapDuration_Responses(
                **default_dict['SetOverlapDuration_Responses']
            )
    
        return return_value
    

    def Subscribe_SwitchingMode(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowConfigurationService_pb2.Subscribe_SwitchingMode_Responses:
        """
        Requests the observable property Switching Mode
            Get the switching mode for syringe pump switchover if one syringe pump runs empty.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.SwitchingMode (Switching Mode): Get the switching mode for syringe pump switchover if one syringe pump runs empty.
        """
    
        # initialise the return value
        return_value: ContinuousFlowConfigurationService_pb2.Subscribe_SwitchingMode_Responses = None
    
        # we could use a timeout here if we wanted
        while True:
            # TODO:
            #   Add implementation of Simulation for property SwitchingMode here and write the resulting
            #   response in return_value
    
            # create the default value
            if return_value is None:
                return_value = ContinuousFlowConfigurationService_pb2.Subscribe_SwitchingMode_Responses(
                    **default_dict['Subscribe_SwitchingMode_Responses']
                )
    
    
            yield return_value
    
    
    def Subscribe_MaxRefillFlowRate(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowConfigurationService_pb2.Subscribe_MaxRefillFlowRate_Responses:
        """
        Requests the observable property Max Refill Flow Rate
            Get the maximum possible refill flow rate for the continuous flow pump.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.MaxRefillFlowRate (Max Refill Flow Rate): Get the maximum possible refill flow rate for the continuous flow pump.
        """
    
        # initialise the return value
        return_value: ContinuousFlowConfigurationService_pb2.Subscribe_MaxRefillFlowRate_Responses = None
    
        # we could use a timeout here if we wanted
        while True:
            # TODO:
            #   Add implementation of Simulation for property MaxRefillFlowRate here and write the resulting
            #   response in return_value
    
            # create the default value
            if return_value is None:
                return_value = ContinuousFlowConfigurationService_pb2.Subscribe_MaxRefillFlowRate_Responses(
                    **default_dict['Subscribe_MaxRefillFlowRate_Responses']
                )
    
    
            yield return_value
    
    
    def Subscribe_RefillFlowRate(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowConfigurationService_pb2.Subscribe_RefillFlowRate_Responses:
        """
        Requests the observable property Refill Flow Rate
            Get the refill flow rate for the continuous flow pump.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.RefillFlowRate (Refill Flow Rate): Get the refill flow rate for the continuous flow pump.
        """
    
        # initialise the return value
        return_value: ContinuousFlowConfigurationService_pb2.Subscribe_RefillFlowRate_Responses = None
    
        # we could use a timeout here if we wanted
        while True:
            # TODO:
            #   Add implementation of Simulation for property RefillFlowRate here and write the resulting
            #   response in return_value
    
            # create the default value
            if return_value is None:
                return_value = ContinuousFlowConfigurationService_pb2.Subscribe_RefillFlowRate_Responses(
                    **default_dict['Subscribe_RefillFlowRate_Responses']
                )
    
    
            yield return_value
    
    
    def Subscribe_MinFlowRate(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowConfigurationService_pb2.Subscribe_MinFlowRate_Responses:
        """
        Requests the observable property Min Flow Rate
            Get the minimum flow rate that is theoretically posible with the continuous flow pump.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.MinFlowRate (Min Flow Rate): Get the minimum flow rate that is theoretically posible with the continuous flow pump.
        """
    
        # initialise the return value
        return_value: ContinuousFlowConfigurationService_pb2.Subscribe_MinFlowRate_Responses = None
    
        # we could use a timeout here if we wanted
        while True:
            # TODO:
            #   Add implementation of Simulation for property MinFlowRate here and write the resulting
            #   response in return_value
    
            # create the default value
            if return_value is None:
                return_value = ContinuousFlowConfigurationService_pb2.Subscribe_MinFlowRate_Responses(
                    **default_dict['Subscribe_MinFlowRate_Responses']
                )
    
    
            yield return_value
    
    
    def Subscribe_CrossFlowDuration(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowConfigurationService_pb2.Subscribe_CrossFlowDuration_Responses:
        """
        Requests the observable property Cross Flow Duration
            Get the cross flow duration for the continuous flow pump.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.CrossFlowDuration (Cross Flow Duration): Get the cross flow duration for the continuous flow pump.
        """
    
        # initialise the return value
        return_value: ContinuousFlowConfigurationService_pb2.Subscribe_CrossFlowDuration_Responses = None
    
        # we could use a timeout here if we wanted
        while True:
            # TODO:
            #   Add implementation of Simulation for property CrossFlowDuration here and write the resulting
            #   response in return_value
    
            # create the default value
            if return_value is None:
                return_value = ContinuousFlowConfigurationService_pb2.Subscribe_CrossFlowDuration_Responses(
                    **default_dict['Subscribe_CrossFlowDuration_Responses']
                )
    
    
            yield return_value
    
    
    def Subscribe_OverlapDuration(self, request, context: grpc.ServicerContext) \
            -> ContinuousFlowConfigurationService_pb2.Subscribe_OverlapDuration_Responses:
        """
        Requests the observable property Overlap Duration
            Get the overlap duration for the continuous flow pump.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.OverlapDuration (Overlap Duration): Get the overlap duration for the continuous flow pump.
        """
    
        # initialise the return value
        return_value: ContinuousFlowConfigurationService_pb2.Subscribe_OverlapDuration_Responses = None
    
        # we could use a timeout here if we wanted
        while True:
            # TODO:
            #   Add implementation of Simulation for property OverlapDuration here and write the resulting
            #   response in return_value
    
            # create the default value
            if return_value is None:
                return_value = ContinuousFlowConfigurationService_pb2.Subscribe_OverlapDuration_Responses(
                    **default_dict['Subscribe_OverlapDuration_Responses']
                )
    
    
            yield return_value
    