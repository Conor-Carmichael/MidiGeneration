from os import getenv
from dotenv import load_dotenv

load_dotenv()

dev_mode = bool(getenv("DEV_MODE", False))


if dev_mode:
    print("Dev Mode Enabled")