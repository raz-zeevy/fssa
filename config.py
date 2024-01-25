import os

MODE_DEBUG = "debug"
MODE_PRODUCTION = "production"
MODE = 'MODE'
INIT_MODE = MODE_PRODUCTION # Possible values: "debug", "production"
os.environ[MODE] = INIT_MODE