import os

MODE_DEBUG = "debug"
MODE_PRODUCTION = "production"
MODE_NO_VALIDATION = "no_validation"
MODE = 'MODE'

INIT_MODE = MODE_PRODUCTION # Possible values: "debug", "production"

os.environ[MODE] = INIT_MODE