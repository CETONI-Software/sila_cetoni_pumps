# Generated by sila2.code_generator; sila2.__version__: 0.10.1
from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import TYPE_CHECKING, Optional, Union

from sila2.server import FeatureImplementationBase, MetadataDict

from .forcemonitoringservice_types import (
    ClearForceSafetyStop_Responses,
    DisableForceMonitoring_Responses,
    EnableForceMonitoring_Responses,
    Force,
    SetForceLimit_Responses,
)

if TYPE_CHECKING:
    from ...server import Server


class ForceMonitoringServiceBase(FeatureImplementationBase, ABC):
    parent_server: Server

    _ForceSensorValue_producer_queue: Queue[Union[Force, Exception]]
    _ForceSensorValue_current_value: Force

    _ForceLimit_producer_queue: Queue[Union[Force, Exception]]
    _ForceLimit_current_value: Force

    _MaxDeviceForce_producer_queue: Queue[Union[Force, Exception]]
    _MaxDeviceForce_current_value: Force

    _ForceMonitoringEnabled_producer_queue: Queue[Union[bool, Exception]]
    _ForceMonitoringEnabled_current_value: bool

    _ForceSafetyStopActive_producer_queue: Queue[Union[bool, Exception]]
    _ForceSafetyStopActive_current_value: bool

    def __init__(self, parent_server: Server):
        """
        Functionality to control the force monitoring, read the force sensor and set a custom force limit for pump devices that support this functionality such as Nemesys S and Nemesys M.
        """
        super().__init__(parent_server=parent_server)

        self._ForceSensorValue_producer_queue = Queue()

        self._ForceLimit_producer_queue = Queue()

        self._MaxDeviceForce_producer_queue = Queue()

        self._ForceMonitoringEnabled_producer_queue = Queue()

        self._ForceSafetyStopActive_producer_queue = Queue()

    def update_ForceSensorValue(self, ForceSensorValue: Force, queue: Optional[Queue[Force]] = None) -> None:
        """
        The currently measured force as read by the force sensor.

        This method updates the observable property 'ForceSensorValue'.

        :param queue: The queue to send updates to. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._ForceSensorValue_producer_queue
            self._ForceSensorValue_current_value = ForceSensorValue
        queue.put(ForceSensorValue)

    def ForceSensorValue_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[Force]]:
        """
        The currently measured force as read by the force sensor.

        This method is called when a client subscribes to the observable property 'ForceSensorValue'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def abort_ForceSensorValue_subscriptions(self, error: Exception, queue: Optional[Queue[Force]] = None) -> None:
        """
        The currently measured force as read by the force sensor.

        This method aborts subscriptions to the observable property 'ForceSensorValue'.

        :param error: The Exception to be sent to the subscribing client.
            If it is no DefinedExecutionError or UndefinedExecutionError, it will be wrapped in an UndefinedExecutionError.
        :param queue: The queue to abort. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._ForceSensorValue_producer_queue
        queue.put(error)

    @property
    def current_ForceSensorValue(self) -> Force:
        try:
            return self._ForceSensorValue_current_value
        except AttributeError:
            raise AttributeError("Observable property ForceSensorValue has never been set")

    def update_ForceLimit(self, ForceLimit: Force, queue: Optional[Queue[Force]] = None) -> None:
        """
        The current force limit.

        This method updates the observable property 'ForceLimit'.

        :param queue: The queue to send updates to. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._ForceLimit_producer_queue
            self._ForceLimit_current_value = ForceLimit
        queue.put(ForceLimit)

    def ForceLimit_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[Force]]:
        """
        The current force limit.

        This method is called when a client subscribes to the observable property 'ForceLimit'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def abort_ForceLimit_subscriptions(self, error: Exception, queue: Optional[Queue[Force]] = None) -> None:
        """
        The current force limit.

        This method aborts subscriptions to the observable property 'ForceLimit'.

        :param error: The Exception to be sent to the subscribing client.
            If it is no DefinedExecutionError or UndefinedExecutionError, it will be wrapped in an UndefinedExecutionError.
        :param queue: The queue to abort. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._ForceLimit_producer_queue
        queue.put(error)

    @property
    def current_ForceLimit(self) -> Force:
        try:
            return self._ForceLimit_current_value
        except AttributeError:
            raise AttributeError("Observable property ForceLimit has never been set")

    def update_MaxDeviceForce(self, MaxDeviceForce: Force, queue: Optional[Queue[Force]] = None) -> None:
        """
        The maximum device force (i.e. the maximum force the pump hardware can take in continuous operation).

        This method updates the observable property 'MaxDeviceForce'.

        :param queue: The queue to send updates to. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._MaxDeviceForce_producer_queue
            self._MaxDeviceForce_current_value = MaxDeviceForce
        queue.put(MaxDeviceForce)

    def MaxDeviceForce_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[Force]]:
        """
        The maximum device force (i.e. the maximum force the pump hardware can take in continuous operation).

        This method is called when a client subscribes to the observable property 'MaxDeviceForce'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def abort_MaxDeviceForce_subscriptions(self, error: Exception, queue: Optional[Queue[Force]] = None) -> None:
        """
        The maximum device force (i.e. the maximum force the pump hardware can take in continuous operation).

        This method aborts subscriptions to the observable property 'MaxDeviceForce'.

        :param error: The Exception to be sent to the subscribing client.
            If it is no DefinedExecutionError or UndefinedExecutionError, it will be wrapped in an UndefinedExecutionError.
        :param queue: The queue to abort. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._MaxDeviceForce_producer_queue
        queue.put(error)

    @property
    def current_MaxDeviceForce(self) -> Force:
        try:
            return self._MaxDeviceForce_current_value
        except AttributeError:
            raise AttributeError("Observable property MaxDeviceForce has never been set")

    def update_ForceMonitoringEnabled(self, ForceMonitoringEnabled: bool, queue: Optional[Queue[bool]] = None) -> None:
        """
        Whether force monitoring is enabled.

        This method updates the observable property 'ForceMonitoringEnabled'.

        :param queue: The queue to send updates to. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._ForceMonitoringEnabled_producer_queue
            self._ForceMonitoringEnabled_current_value = ForceMonitoringEnabled
        queue.put(ForceMonitoringEnabled)

    def ForceMonitoringEnabled_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[bool]]:
        """
        Whether force monitoring is enabled.

        This method is called when a client subscribes to the observable property 'ForceMonitoringEnabled'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def abort_ForceMonitoringEnabled_subscriptions(self, error: Exception, queue: Optional[Queue[bool]] = None) -> None:
        """
        Whether force monitoring is enabled.

        This method aborts subscriptions to the observable property 'ForceMonitoringEnabled'.

        :param error: The Exception to be sent to the subscribing client.
            If it is no DefinedExecutionError or UndefinedExecutionError, it will be wrapped in an UndefinedExecutionError.
        :param queue: The queue to abort. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._ForceMonitoringEnabled_producer_queue
        queue.put(error)

    @property
    def current_ForceMonitoringEnabled(self) -> bool:
        try:
            return self._ForceMonitoringEnabled_current_value
        except AttributeError:
            raise AttributeError("Observable property ForceMonitoringEnabled has never been set")

    def update_ForceSafetyStopActive(self, ForceSafetyStopActive: bool, queue: Optional[Queue[bool]] = None) -> None:
        """
        Whether force safety stop is active.

        This method updates the observable property 'ForceSafetyStopActive'.

        :param queue: The queue to send updates to. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._ForceSafetyStopActive_producer_queue
            self._ForceSafetyStopActive_current_value = ForceSafetyStopActive
        queue.put(ForceSafetyStopActive)

    def ForceSafetyStopActive_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[bool]]:
        """
        Whether force safety stop is active.

        This method is called when a client subscribes to the observable property 'ForceSafetyStopActive'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def abort_ForceSafetyStopActive_subscriptions(self, error: Exception, queue: Optional[Queue[bool]] = None) -> None:
        """
        Whether force safety stop is active.

        This method aborts subscriptions to the observable property 'ForceSafetyStopActive'.

        :param error: The Exception to be sent to the subscribing client.
            If it is no DefinedExecutionError or UndefinedExecutionError, it will be wrapped in an UndefinedExecutionError.
        :param queue: The queue to abort. If None, the default Queue will be used.
        """
        if queue is None:
            queue = self._ForceSafetyStopActive_producer_queue
        queue.put(error)

    @property
    def current_ForceSafetyStopActive(self) -> bool:
        try:
            return self._ForceSafetyStopActive_current_value
        except AttributeError:
            raise AttributeError("Observable property ForceSafetyStopActive has never been set")

    @abstractmethod
    def ClearForceSafetyStop(self, *, metadata: MetadataDict) -> ClearForceSafetyStop_Responses:
        """
        Clear/acknowledge a force safety stop.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def EnableForceMonitoring(self, *, metadata: MetadataDict) -> EnableForceMonitoring_Responses:
        """
        Enable the force monitoring.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def DisableForceMonitoring(self, *, metadata: MetadataDict) -> DisableForceMonitoring_Responses:
        """
        Disable the force monitoring.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def SetForceLimit(self, ForceLimit: Force, *, metadata: MetadataDict) -> SetForceLimit_Responses:
        """
        Set a custom limit.


        :param ForceLimit: The force limit to set. If higher than MaxDeviceForce, MaxDeviceForce will be used instead.

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass
