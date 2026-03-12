# Næste Syn — Home Assistant Integration

Track your vehicle's next periodic inspection and MOT deadline directly in Home Assistant, with countdown sensors and calendar events that update automatically.

Data is fetched from [MotorAPI](https://www.motorapi.dk), which queries the official Danish Motor Register (Motorregistret).

---

## Features

- Sensors for **next inspection date** and **MOT deadline date**, each with a **countdown in days** (negative = overdue)
- Optional sensors: VIN, vehicle use type, make, model, model year, mileage at last MOT
- **Calendar entity** with events for each inspection date — visible in the HA Calendar dashboard and available to automations
- Supports multiple vehicles — add one config entry per registration number
- Refreshes once every 24 hours

---

## Requirements

- A MotorAPI API key — apply at [www.motorapi.dk](https://www.motorapi.dk)
- Home Assistant 2023.1 or newer

---

## Installation

### Via HACS (recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations** → three-dot menu → **Custom repositories**
3. Add `https://github.com/macokay/hacs-naeste-syn` with category **Integration**
4. Install **Næste Syn**
5. Restart Home Assistant

### Manual

Copy the `custom_components/naeste_syn` folder into your HA `custom_components` directory and restart.

---

## Setup

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Næste Syn**
3. Enter your API key and registration number
4. Select which optional sensors to enable
5. Click **Submit**

Optional sensors can be changed at any time via the integration's **Configure** button.

---

## Sensors

| Sensor | Always shown | Description |
|--------|-------------|-------------|
| Registration Number | Yes | The vehicle registration number |
| Next Inspection Date | Yes | ISO date of the next periodic inspection |
| Days Until Next Inspection | Yes | Countdown in days (negative = overdue) |
| MOT Deadline Date | Yes | ISO date of the MOT deadline |
| Days Until MOT Deadline | Yes | Countdown in days |
| VIN | Optional | Vehicle chassis number |
| Vehicle Use | Optional | e.g. "Privat personkørsel" |
| Mileage at Last MOT | Optional | Odometer reading (km) at last MOT |
| Make | Optional | e.g. "AUDI" |
| Model | Optional | e.g. "A6" |
| Model Year | Optional | e.g. 2015 |

---

## Calendar

Each vehicle gets a calendar entity (`calendar.inspection_[registration]`) with events for:

- **Periodic Inspection** — next inspection date
- **MOT Deadline** — MOT deadline date

---

## API field names

The integration uses the following field names from the MotorAPI response (confirmed from [motorapi.dk](https://www.motorapi.dk)):

```
registration_number, vin, make, model, model_year, use,
next_inspection_date, mot_date, mot_mileage
```

If the API uses different field names in a future version, update only the `FIELD_*` constants in `const.py`.

---

## License
© 2026 Mac O Kay
Free to use and modify for personal, non-commercial use.
Credit appreciated if you share or build upon this work.
Commercial use is not permitted.
