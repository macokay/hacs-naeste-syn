"""Constants for the Næste Syn integration."""

DOMAIN = "naeste_syn"

# MotorAPI base URL and vehicle endpoint.
# Confirmed from https://v1.motorapi.dk/doc/
API_BASE_URL = "https://v1.motorapi.dk"
API_ENDPOINT = "/vehicles/{registration}"
API_AUTH_HEADER = "X-AUTH-TOKEN"

# Config entry keys
CONF_API_KEY = "api_key"
CONF_REGISTRATION = "registration_number"

# Optional sensor checkboxes
CONF_SHOW_VIN = "show_vin"
CONF_SHOW_USE = "show_use"
CONF_SHOW_MOT_MILEAGE = "show_mot_mileage"
CONF_SHOW_MAKE = "show_make"
CONF_SHOW_MODEL = "show_model"
CONF_SHOW_MODEL_YEAR = "show_model_year"

# ---------------------------------------------------------------------------
# MotorAPI response field names.
# Confirmed from https://www.motorapi.dk example response:
#   registration_number, status, status_date, type, use, vin,
#   own_weight, total_weight, axels, seats, coupling, doors,
#   make, model, variant, model_type, model_year, color,
#   chassis_type, engine_cylinders, engine_volume, engine_power, fuel_type
#
# Inspection fields (next_inspection_date, mot_date, mot_mileage) are
# assumed present in the full authenticated response. If the API uses
# different names, update only the FIELD_* constants here.
# ---------------------------------------------------------------------------
FIELD_REGISTRATION    = "registration_number"
FIELD_VIN             = "vin"
FIELD_MAKE            = "make"
FIELD_MODEL           = "model"
FIELD_MODEL_YEAR      = "model_year"
FIELD_USE             = "use"
FIELD_NEXT_INSPECTION = "next_inspection_date"
FIELD_MOT_DATE        = "mot_date"
FIELD_MOT_MILEAGE     = "mot_mileage"
