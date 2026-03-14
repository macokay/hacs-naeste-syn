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
# Top-level fields (confirmed from motorapi.dk example response):
#   registration_number, use, vin, make, model, model_year, ...
#
# Inspection fields are nested inside a "mot_info" object:
#   mot_info.date                  -> MOT date (YYYY-MM-DD)
#   mot_info.mileage               -> odometer reading at last MOT
#   mot_info.next_inspection_date  -> next periodic inspection date (YYYY-MM-DD)
# ---------------------------------------------------------------------------

# Top-level fields
FIELD_REGISTRATION    = "registration_number"
FIELD_VIN             = "vin"
FIELD_MAKE            = "make"
FIELD_MODEL           = "model"
FIELD_MODEL_YEAR      = "model_year"
FIELD_USE             = "use"

# Nested mot_info object key
FIELD_MOT_INFO        = "mot_info"

# Keys inside mot_info
FIELD_MOT_DATE        = "date"
FIELD_MOT_MILEAGE     = "mileage"
FIELD_NEXT_INSPECTION = "next_inspection_date"
