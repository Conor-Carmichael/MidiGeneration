from os import getenv
import os
from dotenv import load_dotenv


load_dotenv()

os.environ("PYTHONPATH", "$(PWD)")

project_name = "MusicBase"

log_level = getenv("LOG_LEVEL", "INFO")
dev_mode = bool(getenv("DEV_MODE", False))
