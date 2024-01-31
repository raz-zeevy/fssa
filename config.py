import os

MODE_DEBUG = "debug"
MODE_PRODUCTION = "production"
MODE = 'MODE'
INIT_MODE = MODE_DEBUG # Possible values: "debug", "production"
os.environ[MODE] = INIT_MODE