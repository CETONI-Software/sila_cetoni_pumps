from __future__ import annotations

from typing import cast

from qmixsdk.qmixpump import ContiFlowProperty, ContiFlowPump, ContiFlowSwitchingMode
from sila2.framework import Command
from sila2.framework.errors.validation_error import ValidationError
from sila2.server import MetadataDict, SilaServer

from sila_cetoni.utils import PropertyUpdater, invert_dict, not_close, not_equal

from ..generated.continuousflowconfigurationservice import (
    ContinuousFlowConfigurationServiceBase,
    ContinuousFlowConfigurationServiceFeature,
    SetCrossFlowDuration_Responses,
    SetOverlapDuration_Responses,
    SetRefillFlowRate_Responses,
    SetSwitchingMode_Responses,
)


class ContinuousFlowConfigurationServiceImpl(ContinuousFlowConfigurationServiceBase):
    __pump: ContiFlowPump
    __ALLOWED_SWITCHING_MODES = {
        "SwitchingCrossFlow": ContiFlowSwitchingMode.CROSS_FLOW
        # more to come
    }

    def __init__(self, server: SilaServer, pump: ContiFlowPump):
        super().__init__(server)
        self.__pump = pump

        # TODO restore drive position counter + contiflow params

        self.run_periodically(
            PropertyUpdater(
                lambda: self.__pump.get_device_property(ContiFlowProperty.CROSSFLOW_DURATION_S),
                not_close,
                self.update_CrossFlowDuration,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                lambda: self.__pump.get_device_property(ContiFlowProperty.MAX_REFILL_FLOW),
                not_close,
                self.update_MaxRefillFlowRate,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                lambda: self.__pump.get_device_property(ContiFlowProperty.MIN_PUMP_FLOW),
                not_close,
                self.update_MinFlowRate,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                lambda: self.__pump.get_device_property(ContiFlowProperty.OVERLAP_DURATION_S),
                not_close,
                self.update_OverlapDuration,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                lambda: self.__pump.get_device_property(ContiFlowProperty.REFILL_FLOW),
                not_close,
                self.update_RefillFlowRate,
            )
        )
        self.run_periodically(
            PropertyUpdater(
                lambda: self.__pump.get_device_property(ContiFlowProperty.SWITCHING_MODE),
                not_equal,
                lambda val: self.update_SwitchingMode(invert_dict(self.__ALLOWED_SWITCHING_MODES)[val]),
            )
        )

    def SetSwitchingMode(self, SwitchingMode: str, *, metadata: MetadataDict) -> SetSwitchingMode_Responses:
        if SwitchingMode not in self.__ALLOWED_SWITCHING_MODES:
            err = ValidationError(
                "The given value for the Contiflow Switching Mode is invalid. Allowed values are: "
                + ", ".join(self.__ALLOWED_SWITCHING_MODES.keys())
            )
            err.parameter_fully_qualified_identifier = (
                cast(Command, ContinuousFlowConfigurationServiceFeature["SetSwitchingMode"])
                .parameters.fields[0]
                .fully_qualified_identifier
            )
            raise err

        self.__pump.set_device_property(ContiFlowProperty.SWITCHING_MODE, self.__ALLOWED_SWITCHING_MODES[SwitchingMode])
        return SetSwitchingMode_Responses()

    def SetRefillFlowRate(self, RefillFlowRate: float, *, metadata: MetadataDict) -> SetRefillFlowRate_Responses:
        self.__pump.set_device_property(ContiFlowProperty.REFILL_FLOW, RefillFlowRate)
        return SetRefillFlowRate_Responses()

    def SetCrossFlowDuration(
        self, CrossFlowDuration: float, *, metadata: MetadataDict
    ) -> SetCrossFlowDuration_Responses:
        self.__pump.set_device_property(ContiFlowProperty.CROSSFLOW_DURATION_S, CrossFlowDuration)
        return SetCrossFlowDuration_Responses()

    def SetOverlapDuration(self, OverlapDuration: float, *, metadata: MetadataDict) -> SetOverlapDuration_Responses:
        self.__pump.set_device_property(ContiFlowProperty.OVERLAP_DURATION_S, OverlapDuration)
        return SetOverlapDuration_Responses()
