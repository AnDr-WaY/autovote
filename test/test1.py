import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

options = uc.ChromeOptions()
options.headless = True  # ОБЯЗАТЕЛЬНО True для хостинга! 
options.page_load_strategy = 'eager'
# Дополнительные опции для работы в Linux/Docker на хостинге:
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080') # Иногда помогает

driver = uc.Chrome(options=options, driver_executable_path=uc.find_chrome_executable())
logger.info("Драйвер запущен.")

logger.info("Получаю страницу loliland.ru (eager strategy)")
driver.get("https://loliland.ru/")
driver.quit()