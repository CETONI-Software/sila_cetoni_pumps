from __future__ import annotations

from qmixsdk.qmixpump import Pump
from sila2.framework import Command
from sila2.framework.errors.validation_error import ValidationError

from . import unit_conversion as uc


def validate(
    pump: Pump,
    command: Command,
    flow_rate: float,
    flow_rate_id: int,
    fill_level: float = None,
    fill_level_id: int = None,
    volume: float = None,
    volume_id: int = None,
):
    """
    Validates that the given flow rate and fill level or volume are in the correct ranges for the given `pump`
        :param pump: The pump that provides the bounds for the values
        :param command: The command where the error occurred
        :param flow_rate: The flow rate to check, if it's in the bounds for the given `pump`
        :param flow_rate_id: The index of the FlowRate parameter in the list of parameters
        :param fill_level: The fill level to check, if it's in the bounds for the given `pump`
        :param fill_level_id: The index of the FillLevel parameter in the list of parameters
        :param volume: The volume to check, if it's in the bounds for the given `pump`
        :param volume_id: The index of the Volume parameter in the list of parameters
    """

    current_fill_level = pump.get_fill_level()
    max_fill_level = pump.get_volume_max()
    max_flow_rate = pump.get_flow_rate_max()

    msg = (
        "The requested {param} ({requested_val:.3} {unit}) has to be in the range between 0 {unit} {exclusive} and "
        "{max_val:.3} {unit} for this pump."
    )
    if flow_rate <= 0 or flow_rate > max_flow_rate:
        unit = uc.flow_unit_to_string(pump.get_flow_unit())
        err = ValidationError(
            msg.format(
                param="flow rate",
                unit=unit,
                exclusive="(exclusive)",
                requested_val=flow_rate,
                max_val=max_flow_rate,
            )
        )
        err.parameter_fully_qualified_identifier = command.parameters.fields[flow_rate_id].fully_qualified_identifier
        raise err
    if fill_level is not None and (fill_level < 0 or fill_level > max_fill_level):
        unit = uc.volume_unit_to_string(pump.get_volume_unit())
        err = ValidationError(
            msg.format(param="fill level", unit=unit, exclusive="", requested_val=fill_level, max_val=max_fill_level),
        )
        err.parameter_fully_qualified_identifier = command.parameters.fields[fill_level_id].fully_qualified_identifier
        raise err
    if volume is not None and (
        # negative volume indicates aspiration => current_fill_level + abs(volume) must not be more than max_fill_level
        (volume < 0 and abs(volume) + current_fill_level > max_fill_level)
        # positive volume indicates dispensation => volume must not be more than current_fill_level
        or (volume > 0 and volume > current_fill_level)
        # cannot dose volume of 0
        or volume == 0
    ):
        unit = uc.volume_unit_to_string(pump.get_volume_unit())
        err = ValidationError(
            msg.format(
                param="volume",
                unit=unit,
                exclusive="(exclusive)",
                requested_val=volume,
                max_val=max_fill_level - current_fill_level if volume < 0 else current_fill_level,
            )
        )
        err.parameter_fully_qualified_identifier = command.parameters.fields[volume_id].fully_qualified_identifier
        raise err
