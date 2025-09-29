from dotenv import dotenv_values

config = dotenv_values(".env")

BOT_API_KEY = config.get("BOT_API_KEY")
ADMIN_ID = config.get("ADMIN_ID")


YDB_ENDPOINT = config.get("YDB_ENDPOINT")
YDB_PATH = config.get("YDB_PATH")
YDB_TOKEN = config.get("YDB_TOKEN")
