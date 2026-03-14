# Changelog

## [1.0.1] - 2026-03-13

### Fixed
- Corrected MotorAPI base URL to `https://v1.motorapi.dk`
- Corrected authentication header from `X-API-Key` to `X-AUTH-TOKEN`
- Corrected vehicle endpoint to `/vehicles/{registration}`

## [1.0.0] - 2026-03-12

### Added
- Initial release
- Sensors: registration number, next inspection date + countdown, MOT deadline date + countdown
- Optional sensors: VIN, vehicle use type, mileage at last MOT, make, model, model year
- Calendar entity with events for periodic inspection and MOT deadline
- Config flow with options flow for managing optional sensors
- Danish and English translations
