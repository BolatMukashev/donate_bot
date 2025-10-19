from dotenv import dotenv_values

config = dotenv_values(".env")

BOT_API_KEY = config.get("BOT_API_KEY")
ADMIN_ID = int(config.get("ADMIN_ID"))


YDB_ENDPOINT = config.get("YDB_ENDPOINT")
YDB_PATH = config.get("YDB_PATH")
YDB_TOKEN = config.get("YDB_TOKEN")


START_IMAGE = 'AgACAgIAAxkBAAMYaPNyloVz7bI3vAqvG23N_xgKHCMAAmj4MRtVnqBLipazNxMXVDwBAAMCAAN5AAM2BA'
