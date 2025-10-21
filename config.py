import os
from dotenv import dotenv_values

config = dotenv_values(".env")

BOT_API_KEY = os.environ.get("BOT_API_KEY") or config.get("BOT_API_KEY")
ADMIN_ID = int(os.environ.get("ADMIN_ID")) if os.environ.get("ADMIN_ID") else int(config.get("ADMIN_ID"))
ASTANA_ID = int(os.environ.get("ASTANA_ID")) if os.environ.get("ASTANA_ID") else int(config.get("ASTANA_ID"))

ADMINS = [ADMIN_ID, ASTANA_ID]


YDB_ENDPOINT = os.environ.get("YDB_ENDPOINT") or config.get("YDB_ENDPOINT")
YDB_PATH = os.environ.get("YDB_PATH") or config.get("YDB_PATH")
YDB_TOKEN = os.environ.get("YDB_TOKEN") or config.get("YDB_TOKEN")


START_IMAGE = 'AgACAgIAAxkBAAMYaPNyloVz7bI3vAqvG23N_xgKHCMAAmj4MRtVnqBLipazNxMXVDwBAAMCAAN5AAM2BA'
