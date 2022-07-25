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
