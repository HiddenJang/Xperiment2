import os
from pathlib import Path
from dotenv import read_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# .env path
ENV_PATH = BASE_DIR / 'client_app.env'

# env variables load
if os.path.exists(ENV_PATH):
    read_dotenv(dotenv=ENV_PATH)

# Logging settings
FORMAT = "%(asctime)s -- %(name)s -- %(lineno)s -- %(levelname)s -- %(message)s"
LOGS_PATH = BASE_DIR / "logs"
FILENAME = LOGS_PATH / "gui_logs.log"
LOGLEVEL = "DEBUG"
MAX_BYTES_FILE_SIZE = 300000
LOG_FILES_COUNT = 10

# Default server api
DEFAULT_API_URL = 'http://127.0.0.1:8000/api/v1/start/'

# Bookmakers
BOOKMAKERS = {'betboom': 'https://betboom.ru/',
              'leon': 'https://leon.ru/',
              'olimp': 'https://www.olimp.bet/',
              'xstavka': 'https://1xstavka.ru/'}

# Result extraction settings
RESULT_EXTRACTION_CLASSES = {'API': 'ApiResponseParser',
                             'SELENIUM': 'SeleniumParser'}
RESULTS_URL = {'olimp': 'https://www.olimp.bet/results?sportId=%d&startDate=%s&endDate=%s&shouldSearchByChamps=false'}

# Webdriver settings
# directory (base dir /--/ browsers_control)
WEBDRIVER_DIR = {'linux': BASE_DIR / "components/browsers_control/chromedriver/chromedriver",
                 'win32': BASE_DIR / "components\\browsers_control\\chromedriver\\chromedriver.exe"}

# Screenshots directory
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Statistic settings
STATS_DIR = BASE_DIR / "statistic"
STATS_FILE_NAME = STATS_DIR / "statistic.xlsx"
