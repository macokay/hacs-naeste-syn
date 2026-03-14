# Changelog

## [1.0.4] - 2026-03-14

### Changed
- Reordered sensors: Days Until Next Inspection, Next Inspection Date, Last Inspection Date, Mileage at Last Inspection, VIN, Registration Number, Make, Model, Model Year, Vehicle Use
- Renamed "Last MOT Date" to "Last Inspection Date"
- Renamed "Mileage at Last MOT" to "Mileage at Last Inspection"
- Updated README to reflect current sensor set and API structure

## [1.0.3] - 2026-03-14

### Changed
- Renamed "MOT Deadline Date" to "Last MOT Date" to correctly reflect the field
- Removed "Days Until MOT Deadline" sensor

## [1.0.2] - 2026-03-14

### Fixed
- MOT fields (date, mileage, next inspection date) now correctly extracted from nested `mot_info` object in the MotorAPI response
- Calendar events now read from `mot_info` sub-object

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
