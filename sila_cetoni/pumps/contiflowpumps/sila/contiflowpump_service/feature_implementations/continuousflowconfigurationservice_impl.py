from __future__ import annotations

import math
import time
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict

from qmixsdk.qmixpump import ContiFlowProperty, ContiFlowPump, ContiFlowSwitchingMode
from sila2.framework import FullyQualifiedIdentifier
from sila2.framework.errors.validation_error import ValidationError
from sila2.server import MetadataDict, SilaServer

from ..generated.continuousflowconfigurationservice import (
    ContinuousFlowConfigurationServiceBase,
    ContinuousFlowConfigurationServiceFeature,
    SetCrossFlowDuration_Responses,
    SetOverlapDuration_Responses,
    SetRefillFlowRate_Responses,
    SetSwitchingMode_Responses,
)


def invert_dict(d: dict) -> dict:
    return dict([(v, k) for k, v in d.items()])


class ContinuousFlowConfigurationServiceImpl(ContinuousFlowConfigurationServiceBase):
    __pump: ContiFlowPump
    __ALLOWED_SWITCHING_MODES = {
        "SwitchingCrossFlow": ContiFlowSwitchingMode.CROSS_FLOW
        # more to come
    }
    __stop_event: Event

    def __init__(self, server: SilaServer, pump: ContiFlowPump, executor: Executor):
        super().__init__(server)
        self.__pump = pump
        self.__stop_event = Event()

        # TODO restore drive position counter + contiflow params

        def update_cross_flow_duration(stop_event: Event):
            new_cross_flow_duration = cross_flow_duration = self.__pump.get_device_property(
                ContiFlowProperty.CROSSFLOW_DURATION_S
            )
            while not stop_event.is_set():
                new_cross_flow_duration = self.__pump.get_device_property(ContiFlowProperty.CROSSFLOW_DURATION_S)
                if not math.isclose(new_cross_flow_duration, cross_flow_duration):
                    self.update_CrossFlowDuration(cross_flow_duration)
                time.sleep(0.1)

        def update_max_refill_flow(stop_event: Event):
            new_max_refill_flow = max_refill_flow = self.__pump.get_device_property(ContiFlowProperty.MAX_REFILL_FLOW)
            while not stop_event.is_set():
                new_max_refill_flow = self.__pump.get_device_property(ContiFlowProperty.MAX_REFILL_FLOW)
                if not math.isclose(new_max_refill_flow, max_refill_flow):
                    self.update_MaxRefillFlowRate(max_refill_flow)
                time.sleep(0.1)

        def update_min_flow_rate(stop_event: Event):
            new_min_flow_rate = min_flow_rate = self.__pump.get_device_property(ContiFlowProperty.MIN_PUMP_FLOW)
            while not stop_event.is_set():
                new_min_flow_rate = self.__pump.get_device_property(ContiFlowProperty.MIN_PUMP_FLOW)
                if not math.isclose(new_min_flow_rate, min_flow_rate):
                    self.update_MinFlowRate(min_flow_rate)
                time.sleep(0.1)

        def update_overlap_duration(stop_event: Event):
            new_overlap_duration = overlap_duration = self.__pump.get_device_property(
                ContiFlowProperty.OVERLAP_DURATION_S
            )
            while not stop_event.is_set():
                new_overlap_duration = self.__pump.get_device_property(ContiFlowProperty.OVERLAP_DURATION_S)
                if not math.isclose(new_overlap_duration, overlap_duration):
                    self.update_OverlapDuration(overlap_duration)
                time.sleep(0.1)

        def update_refill_flow_rate(stop_event: Event):
            new_refill_flow_rate = refill_flow_rate = self.__pump.get_device_property(ContiFlowProperty.REFILL_FLOW)
            while not stop_event.is_set():
                new_refill_flow_rate = self.__pump.get_device_property(ContiFlowProperty.REFILL_FLOW)
                if not math.isclose(new_refill_flow_rate, refill_flow_rate):
                    self.update_RefillFlowRate(refill_flow_rate)
                time.sleep(0.1)

        def update_switching_mode(stop_event: Event):
            new_switching_mode = switching_mode = self.__pump.get_device_property(ContiFlowProperty.SWITCHING_MODE)
            while not stop_event.is_set():
                new_switching_mode = self.__pump.get_device_property(ContiFlowProperty.SWITCHING_MODE)
                if new_switching_mode != switching_mode:
                    self.update_SwitchingMode(invert_dict(self.__ALLOWED_SWITCHING_MODES)[switching_mode])
                time.sleep(0.1)

        # initial values
        self.update_CrossFlowDuration(self.__pump.get_device_property(ContiFlowProperty.CROSSFLOW_DURATION_S))
        self.update_MaxRefillFlowRate(self.__pump.get_device_property(ContiFlowProperty.MAX_REFILL_FLOW))
        self.update_MinFlowRate(self.__pump.get_device_property(ContiFlowProperty.MIN_PUMP_FLOW))
        self.update_OverlapDuration(self.__pump.get_device_property(ContiFlowProperty.OVERLAP_DURATION_S))
        self.update_RefillFlowRate(self.__pump.get_device_property(ContiFlowProperty.REFILL_FLOW))
        self.update_SwitchingMode(invert_dict(self.__ALLOWED_SWITCHING_MODES).get(ContiFlowProperty.SWITCHING_MODE))

        executor.submit(update_cross_flow_duration, self.__stop_event)
        executor.submit(update_max_refill_flow, self.__stop_event)
        executor.submit(update_min_flow_rate, self.__stop_event)
        executor.submit(update_overlap_duration, self.__stop_event)
        executor.submit(update_refill_flow_rate, self.__stop_event)
        executor.submit(update_switching_mode, self.__stop_event)

    def SetSwitchingMode(self, SwitchingMode: str, *, metadata: MetadataDict) -> SetSwitchingMode_Responses:
        try:
            self.__pump.set_device_property(
                ContiFlowProperty.SWITCHING_MODE, self.__ALLOWED_SWITCHING_MODES.get(SwitchingMode)
            )
        except KeyError:
            err = ValidationError(
                "The given value for the Contiflow Switching Mode is invalid. Allowed values are: "
                + ", ".join(self.__ALLOWED_SWITCHING_MODES.keys())
            )
            err.parameter_fully_qualified_identifier = (
                ContinuousFlowConfigurationServiceFeature["SetSwitchingMode"]
                .parameters.fields[0]
                .fully_qualified_identifier
            )
            raise err

    def SetRefillFlowRate(self, RefillFlowRate: float, *, metadata: MetadataDict) -> SetRefillFlowRate_Responses:
        self.__pump.set_device_property(ContiFlowProperty.REFILL_FLOW, RefillFlowRate)

    def SetCrossFlowDuration(
        self, CrossFlowDuration: float, *, metadata: MetadataDict
    ) -> SetCrossFlowDuration_Responses:
        self.__pump.set_device_property(ContiFlowProperty.CROSSFLOW_DURATION_S, CrossFlowDuration)

    def SetOverlapDuration(self, OverlapDuration: float, *, metadata: MetadataDict) -> SetOverlapDuration_Responses:
        self.__pump.set_device_property(ContiFlowProperty.OVERLAP_DURATION_S, OverlapDuration)

    def stop(self) -> None:
        super().stop()
        self.__stop_event.set()
