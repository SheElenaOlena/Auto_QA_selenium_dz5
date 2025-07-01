import time

# Задание 2: Тестирование Drag & Drop (Перетаскивание изображения в корзину)
# Открыть страницу Drag & Drop Demo.
# Перейти по ссылке: https://www.globalsqa.com/demo-site/draganddrop/.
# Выполнить следующие шаги:
# Захватить первую фотографию (верхний левый элемент).
# Перетащить её в область корзины (Trash).
# Проверить, что после перемещения:
# В корзине появилась одна фотография.
# В основной области осталось 3 фотографии.
# Ожидаемый результат:
# Фотография успешно перемещается в корзину.
# Вне корзины остаются 3 фотографии.
#
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService



# Фикстура WebDriver
@pytest.fixture
def driver():
    options = webdriver.FirefoxOptions()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=options
    )
    driver.maximize_window()
    driver.quit()


def test_drag_and_drop_image(driver):
    wait = WebDriverWait(driver, 15)
    driver.get('https://www.globalsqa.com/demo-site/draganddrop/')
    time.sleep(3)
    # 2) Дождаться, пока кнопка "Согласиться" станет кликабельной
    consent_button = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        "button.fc-cta-consent"
    )))
    consent_button.click()

    # 👉 Ждём появления и переключаемся в iframe
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.demo-frame")))
    driver.switch_to.frame(iframe)

    # Элемент для перетаскивания (первая фотография)
    draggable = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#gallery > li:nth-child(1) > img')))
    droppable = wait.until(EC.presence_of_element_located((By.ID, "trash")))

    # Drag and Drop
    actions = ActionChains(driver)
    actions.drag_and_drop(draggable, droppable).pause(2).perform()

    # Проверка: В корзине 1 фото
    trash_image = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#trash li")))
    assert len(trash_image) == 1, "В корзине должно быть 1 изображение"

    # Проверка: В галерее осталось 3 фото
    gallery_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#gallery > li")))
    assert len(gallery_items) == 3, "В галерее должно остаться 3 изображения"







