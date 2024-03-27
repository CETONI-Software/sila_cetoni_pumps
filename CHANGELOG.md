# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Types of changes

    `Added` for new features.
    `Changed` for changes in existing functionality.
    `Deprecated` for soon-to-be removed features.
    `Removed` for now removed features.
    `Fixed` for any bug fixes.
    `Security` in case of vulnerabilities.
-->

## Unreleased

### Fixed

- Fix wrong UndefinedExecutionError when calling another dosage Command during a running dosage

## v1.9.1

Sync with sila_cetoni v1.9.1 release

## v1.9.0

Sync with sila_cetoni v1.9.0 release

### Changed

- Don't set the Command Execution status explicitly - this is done by sila_python
- `ApplicationSystem.ensure_operational` is now used instead of manually checking the `ApplicationSystem`'s state
- All syringe pump features are now monitored for traffic by `CetoniApplicationSystem`

### Fixed

- Error when the pump didn't start pumping because ot was already at the target volume
- Invalid Command Execution Progress Info value

## v1.8.0

Sync with sila_cetoni v1.8.0 release

### Changed

- Bump required sila2 version to v0.10.1
- Increase required Python version to 3.8 because in 3.7 the implementation of `ThreadPoolExecutor` in the standard library does not reuse idle threads leading to an ever increasing number of threads which eventually causes blocking of the server(s) on Raspberry Pis

## v1.7.1

Sync with sila_cetoni v1.7.1 release

### Fixed

- Typo in pyproject.toml

## v1.7.0

Sync with sila_cetoni v1.7.0

### Changed

- Bump required sila2 version to v0.10.0

### Fixed

- Progress values of Observable Commands are now correctly bound between 0 and 1

## v1.6.0

Sync with sila_cetoni v1.6.0

## v1.5.0

Sync with sila_cetoni v1.5.0

## v1.4.0

Sync with sila_cetoni v1.4.0

### Fixed

- Raising of `ValidationError`s works again
- Validation of PumpFluidDosingService/Command/DoseVolume/Parameter/Volume
- Setting the initial property values of PumpDriveControlService

## v1.3.0

Sync with sila_cetoni v1.3.0

### Fixed

- Properly call `super().stop()` in the feature implementation classes

## v1.2.0

Sync with sila_cetoni v1.2.0

### Changed

- Use the server name as the name for `ServerConfiguration`

## v1.1.0

### Changed

- Bump sila2 to v0.8.2

### Fixed

- When calling the `EnablePumpDrive`/`DisablePumpDrive` Commands the `PumpDriveState` Property is updated to immediately
  reflect the new state

## v1.0.0

First release of sila_cetoni

This is the pumps plugin which adds support for controlling CETONI syringe and contiflow pump devices via SiLA 2

### Added

- ForceMonitoringService feature and feature implementation
- PumpDriveControlService feature and feature implementation
- PumpFluidDosingService feature and feature implementation
- PumpUnitController feature and feature implementation
- SyringeConfiguration feature and feature implementation
- ContinuousFlowConfigurationService feature and feature implementation
- ContinuousFlowDosingService feature and feature implementation
- ContinuousFlowInitializationService feature and feature implementation
