
# Задание 1: Проверка наличия текста в iframe
# Открыть страницу
# Перейти по ссылке: https://bonigarcia.dev/selenium-webdriver-java/iframes.html.
# Проверить наличие текста
# Найти фрейм (iframe), в котором содержится искомый текст.
# Переключиться в этот iframe.
# Найти элемент, содержащий текст "semper posuere integer et senectus justo curabitur.".
# Убедиться, что текст отображается на странице.

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import TimeoutException



@pytest.fixture
def browser():
    options = webdriver.FirefoxOptions()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()

def test_iframe_text_presence(browser):
    browser.get("https://bonigarcia.dev/selenium-webdriver-java/iframes.html")
    wait = WebDriverWait(browser, 10)

    # Получаем все iframe на странице
    iframes = browser.find_elements(By.TAG_NAME, "iframe")


    # Проверяем наличие нужного текста
    found = False

    for frame in iframes:
        browser.switch_to.frame(frame)
        try:
            element = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'semper posuere')]"))
            )
            found = True
            browser.switch_to.default_content()
            break
        except TimeoutException:
            browser.switch_to.default_content()
            continue

    assert found, "Текст не найден ни в одном iframe"

    # Возвращаемся в основной контент
    browser.switch_to.default_content()
