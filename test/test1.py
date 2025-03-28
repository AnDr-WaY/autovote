import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import sys
import io
import logging 
from django.conf import settings


# Настраиваем базовый логгер
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_loliland_bonus_script(username: str, password: str):
    logger.info("Запуск скрипта LoliLand Bonus...")
    options = uc.ChromeOptions()
    options.headless = True  # ОБЯЗАТЕЛЬНО True для хостинга! 
    options.page_load_strategy = 'eager'
    # Дополнительные опции для работы в Linux/Docker на хостинге:
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080') # Иногда помогает

    driver = None # Инициализируем driver как None
    try:
        # Используйте uc.find_chrome_executable() если chromedriver не в PATH
        # driver = uc.Chrome(options=options, driver_executable_path=uc.find_chrome_executable())
        driver = uc.Chrome(options=options)
        logger.info("Драйвер запущен.")

        logger.info("Получаю страницу loliland.ru (eager strategy)")
        driver.get("https://loliland.ru/")

        wait = WebDriverWait(driver, 15) 
        time.sleep(4)
        logger.info("Ищу поле логина")
        login_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Логин']")))
        login_field.send_keys(username) 
        time.sleep(2)
        logger.info("Ищу поле пароля")
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Пароль']")))
        password_field.send_keys(password) 
        time.sleep(1)

        # --- Логика повторных попыток входа ---
        max_retries = 3
        retry_count = 0
        login_successful = False
        element_after_login = None

        while retry_count <= max_retries and not login_successful:
            try:
                logger.info(f"Попытка входа #{retry_count + 1}...")
                # Находим кнопку перед каждым кликом (на случай, если элемент устарел)
                login_button_xpath = "//div[@class='btn-drop' and contains(normalize-space(), 'Войти')]"
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, login_button_xpath))
                )
                login_button.click()
                logger.info("Кнопка 'Войти' нажата.")

                # Ждем элемент подтверждения с коротким таймаутом (5 секунд)
                logger.info("Ожидаю элемент подтверждения входа (таймаут 5 сек)...")
                confirmation_wait = WebDriverWait(driver, 5) # Короткий таймаут для проверки
                element_after_login = confirmation_wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'AnDr_WaY')]")) # Ваш селектор подтверждения
                )
                logger.info("Элемент подтверждения найден.")
                login_successful = True # Успех, выходим из цикла

            except TimeoutException:
                logger.warning(f"Элемент подтверждения не найден за 5 секунд после попытки #{retry_count + 1}.")
                retry_count += 1
                if retry_count <= max_retries:
                    logger.info(f"Повторная попытка через 5 секунд... (Осталось {max_retries - retry_count + 1})")
                    time.sleep(5) # Пауза перед следующей попыткой
                else:
                    logger.error("Достигнуто максимальное количество попыток входа. Вход не удался.")
                    # Выходим из цикла после последней неудачной попытки
                    break

            except Exception as e:
                # Ловим другие возможные ошибки (например, кнопка не найдена)
                logger.error(f"Произошла неожиданная ошибка во время попытки входа #{retry_count + 1}: {e}", exc_info=True)
                retry_count += 1
                if retry_count <= max_retries:
                    logger.info(f"Повторная попытка через 5 секунд из-за ошибки... (Осталось {max_retries - retry_count + 1})")
                    time.sleep(5)
                else:
                    logger.error("Достигнуто максимальное количество попыток входа из-за ошибки.")
                    break # Выходим из цикла
        # --- Конец логики повторных попыток ---
        
        time.sleep(11)
        # --- Действия после входа (выполняются только если login_successful == True) ---
        if login_successful and element_after_login:
            logger.info("Вход успешно подтвержден.")

            logger.info("Перехожу на страницу бонуса (eager strategy)")
            driver.get("https://loliland.ru/bonus")

            try:
                logger.info("Ожидаю кнопку бонуса...")
                # Уточните селектор кнопки бонуса!
                bonus_button = WebDriverWait(driver, 15).until( # Увеличим ожидание для кнопки бонуса
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='give']")) # Пример, проверьте актуальный XPath
                )
                logger.info("Кнопка бонуса найдена, нажимаю.")
                bonus_button.click()
                time.sleep(3) # Пауза после клика
                logger.info("Кнопка бонуса нажата.")

            except Exception as e_bonus:
                 logger.error(f"Не удалось найти или нажать кнопку бонуса: {e_bonus}", exc_info=True)
                 # Можно сделать скриншот страницы бонуса при ошибке
                 if driver:
                     try:
                        timestamp = time.strftime("%Y%m%d-%H%M%S")
                        filename = f"bonus_page_error_{timestamp}.png"
                        driver.save_screenshot(filename)
                        logger.info(f"Скриншот ошибки страницы бонуса сохранен как {filename}")
                     except Exception as screenshot_error:
                        logger.error(f"Не удалось сохранить скриншот страницы бонуса: {screenshot_error}")

        else:
            # Если цикл завершился без успеха
            logger.error("Не удалось войти на сайт после всех попыток. Пропускаю получение бонуса.")
            # Сохраняем скриншот финальной неудачи входа
            if driver:
                 try:
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    filename = f"login_failure_screenshot_{timestamp}.png"
                    driver.save_screenshot(filename)
                    logger.info(f"Скриншот ошибки входа сохранен как {filename}")
                 except Exception as screenshot_error:
                    logger.error(f"Не удалось сохранить скриншот ошибки входа: {screenshot_error}")
            # Скрипт продолжит выполнение и перейдет к блоку finally для закрытия драйвера

    except Exception as e:
        logger.error(f"Глобальная ошибка во время выполнения скрипта: {e}", exc_info=True)
        if driver:
            try:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"global_error_screenshot_{timestamp}.png"
                driver.save_screenshot(filename)
                logger.info(f"Скриншот глобальной ошибки сохранен как {filename}")
            except Exception as screenshot_error:
                logger.error(f"Не удалось сохранить скриншот глобальной ошибки: {screenshot_error}")

    finally:
        if driver:
            logger.info("Завершаю работу и закрываю браузер.")
            original_stderr = sys.stderr
            sys.stderr = io.StringIO() # Подавляем ошибку __del__
            try:
                driver.quit()
            except Exception as e_quit:
                original_stderr.write(f"Ошибка при вызове driver.quit(): {e_quit}\n")
            finally:
                sys.stderr = original_stderr
        logger.info("Скрипт LoliLand Bonus завершен.")
        
if __name__ == "__main__":
    run_loliland_bonus_script("AnDr_WaY", '')