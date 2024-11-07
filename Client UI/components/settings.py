from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Logging settings
FORMAT = "%(asctime)s -- %(name)s -- %(lineno)s -- %(levelname)s -- %(message)s"
LOGS_PATH = BASE_DIR / "logs"
FILENAME = LOGS_PATH / "gui_logs.log"
LOGLEVEL = "DEBUG"

# Default server api
DEFAULT_API_URL = 'http://127.0.0.1:8000/api/v1/start/'

# Bookmakers
BOOKMAKERS = {
    'betboom': 'https://betboom.ru/',
    'leon': 'https://leon.ru/',
    'olimp': 'https://www.olimp.bet/',
    'xstavka': 'https://1xstavka.ru/',
}

# Webdriver directory (base dir - browsers_control)
WEBDRIVER_DIR = {
    'linux': BASE_DIR / "components/browsers_control/chromedriver/chromedriver",
    'windows': BASE_DIR / "components\\browsers_control\\chromedriver\\chromedriver.exe"
}
