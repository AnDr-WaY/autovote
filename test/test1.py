import undetected_chromedriver as uc
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    options = uc.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    logger.info("Драйвер запущен успешно!")
    driver.get("https://www.google.com")
    logger.info(f"Заголовок страницы: {driver.title}")
    driver.quit()
except Exception as e:
    logger.error(f"Ошибка при запуске драйвера: {e}")