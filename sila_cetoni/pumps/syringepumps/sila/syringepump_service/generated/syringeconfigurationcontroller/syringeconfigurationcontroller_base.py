# Generated by sila2.code_generator; sila2.__version__: 0.10.1
from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import TYPE_CHECKING, Optional, Union

from sila2.server import FeatureImplementationBase, MetadataDict

from .syringeconfigurationcontroller_types import SetSyringeParameters_Responses

if TYPE_CHECKING:
    from ...server import Server


class SyringeConfigurationControllerBase(FeatureImplementationBase, ABC):
    parent_server: Server

    _InnerDiameter_producer_queue: Queue[Union[float, Exception]]
    _InnerDiameter_current_value: float

    _MaxPistonStroke_producer_queue: Queue[Union[float, Exception]]
    _MaxPistonStroke_current_value: float

    def __init__(self, parent_server: Server):
        """
        Provides syringe pump specific functions for configuration (i.e. the configuration of the syringe itself).
        """
        super().__init__(parent_server=parent_server)

        self._InnerDiameter_producer_queue = Queue()

        self._MaxPistonStroke_producer_queue = Queue()

    def update_InnerDiameter(self, InnerDiameter: float, queue: Optional[Queue[float]] = None) -> None:
        """
        Inner diameter of the syringe tube in millimetres.

        This method updates the observable property 'InnerDiameter'.

        :param queue: The queue to send updates to. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._InnerDiameter_producer_queue
            self._InnerDiameter_current_value = InnerDiameter
        queue.put(InnerDiameter)

    def InnerDiameter_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[float]]:
        """
        Inner diameter of the syringe tube in millimetres.

        This method is called when a client subscribes to the observable property 'InnerDiameter'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def abort_InnerDiameter_subscriptions(self, error: Exception, queue: Optional[Queue[float]] = None) -> None:
        """
        Inner diameter of the syringe tube in millimetres.

        This method aborts subscriptions to the observable property 'InnerDiameter'.

        :param error: The Exception to be sent to the subscribing client.
            If it is no DefinedExecutionError or UndefinedExecutionError, it will be wrapped in an UndefinedExecutionError.
        :param queue: The queue to abort. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._InnerDiameter_producer_queue
        queue.put(error)

    @property
    def current_InnerDiameter(self) -> float:
        try:
            return self._InnerDiameter_current_value
        except AttributeError:
            raise AttributeError("Observable property InnerDiameter has never been set")

    def update_MaxPistonStroke(self, MaxPistonStroke: float, queue: Optional[Queue[float]] = None) -> None:
        """
        The maximum piston stroke defines the maximum position the piston can be moved to before it slips out of the syringe tube. The maximum piston stroke limits the maximum travel range of the syringe pump pusher.

        This method updates the observable property 'MaxPistonStroke'.

        :param queue: The queue to send updates to. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._MaxPistonStroke_producer_queue
            self._MaxPistonStroke_current_value = MaxPistonStroke
        queue.put(MaxPistonStroke)

    def MaxPistonStroke_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[float]]:
        """
        The maximum piston stroke defines the maximum position the piston can be moved to before it slips out of the syringe tube. The maximum piston stroke limits the maximum travel range of the syringe pump pusher.

        This method is called when a client subscribes to the observable property 'MaxPistonStroke'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def abort_MaxPistonStroke_subscriptions(self, error: Exception, queue: Optional[Queue[float]] = None) -> None:
        """
        The maximum piston stroke defines the maximum position the piston can be moved to before it slips out of the syringe tube. The maximum piston stroke limits the maximum travel range of the syringe pump pusher.

        This method aborts subscriptions to the observable property 'MaxPistonStroke'.

        :param error: The Exception to be sent to the subscribing client.
            If it is no DefinedExecutionError or UndefinedExecutionError, it will be wrapped in an UndefinedExecutionError.
        :param queue: The queue to abort. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._MaxPistonStroke_producer_queue
        queue.put(error)

    @property
    def current_MaxPistonStroke(self) -> float:
        try:
            return self._MaxPistonStroke_current_value
        except AttributeError:
            raise AttributeError("Observable property MaxPistonStroke has never been set")

    @abstractmethod
    def SetSyringeParameters(
        self, InnerDiameter: float, MaxPistonStroke: float, *, metadata: MetadataDict
    ) -> SetSyringeParameters_Responses:
        """
        Set syringe parameters.
            If you change the syringe in one device, you need to setup the new syringe parameters to get proper conversion of flow rate und volume units.


        :param InnerDiameter: Inner diameter of the syringe tube in millimetres.

        :param MaxPistonStroke: The maximum piston stroke defines the maximum position the piston can be moved to before it slips out of the syringe tube. The maximum piston stroke limits the maximum travel range of the syringe pump pusher.

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass
