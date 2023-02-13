from os import getenv
from dotenv import load_dotenv


load_dotenv()


project_name = "MusicBase"

log_level = getenv("LOG_LEVEL", "INFO")
dev_mode = bool(getenv("DEV_MODE", False))