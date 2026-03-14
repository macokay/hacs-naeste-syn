# Næste Syn — Home Assistant Integration

Track your vehicle's next periodic inspection directly in Home Assistant, with a countdown sensor and calendar events that update automatically.

Data is fetched from [MotorAPI](https://www.motorapi.dk), which queries the official Danish Motor Register (Motorregistret).

---

## Features

- Countdown sensor showing **days until next inspection** (negative = overdue)
- Sensors for **next inspection date** and **last inspection date**
- Optional sensors: mileage at last inspection, VIN, make, model, model year, vehicle use type
- **Calendar entity** with an event for the next inspection — visible in the HA Calendar dashboard and available to automations
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
| Days Until Next Inspection | Yes | Countdown in days (negative = overdue) |
| Next Inspection Date | Yes | Date of the next periodic inspection (ISO) |
| Last Inspection Date | Yes | Date of the most recent inspection (ISO) |
| Mileage at Last Inspection | Optional | Odometer reading (km) at last inspection |
| VIN | Optional | Vehicle chassis number |
| Registration Number | Yes | The vehicle registration number |
| Make | Optional | e.g. "OPEL" |
| Model | Optional | e.g. "ASTRA" |
| Model Year | Optional | e.g. 2017 |
| Vehicle Use | Optional | e.g. "Privat personkørsel" |

---

## Calendar

Each vehicle gets a calendar entity (`calendar.inspection_[registration]`) with an event for the **next periodic inspection** date. The event appears in the HA Calendar dashboard and can be used in automations.

---

## API field names

The integration uses the following fields from the MotorAPI response (confirmed from [motorapi.dk](https://www.motorapi.dk)):

Top-level fields: `registration_number`, `vin`, `make`, `model`, `model_year`, `use`

Inspection fields are nested under `mot_info`:

```json
"mot_info": {
  "date": "2025-09-10",
  "mileage": 163000,
  "next_inspection_date": "2027-09-10"
}
```

If the API uses different field names in a future version, update only the `FIELD_*` constants in `const.py`.

---

## License
© 2026 Mac O Kay
Free to use and modify for personal, non-commercial use.
Credit appreciated if you share or build upon this work.
Commercial use is not permitted.
