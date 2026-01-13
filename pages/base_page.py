from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Базовый класс для всех Page Objects."""
    
    def __init__(self, driver):
        """
        Инициализация базовой страницы.
        
        Args:
            driver: Экземпляр WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        """
        Поиск элемента с явным ожиданием.
        
        Args:
            locator: Кортеж (By, value) для локатора
            
        Returns:
            WebElement: Найденный элемент
        """
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """
        Поиск элементов с явным ожиданием.
        
        Args:
            locator: Кортеж (By, value) для локатора
            
        Returns:
            List[WebElement]: Список найденных элементов
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click_element(self, locator):
        """
        Клик по элементу с явным ожиданием кликабельности.
        
        Args:
            locator: Кортеж (By, value) для локатора
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def send_keys(self, locator, text):
        """
        Ввод текста в элемент с явным ожиданием видимости.
        
        Args:
            locator: Кортеж (By, value) для локатора
            text: Текст для ввода
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """
        Получение текста элемента с явным ожиданием видимости.
        
        Args:
            locator: Кортеж (By, value) для локатора
            
        Returns:
            str: Текст элемента
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text
    
    def is_element_visible(self, locator, timeout=10):
        """
        Проверка видимости элемента.
        
        Args:
            locator: Кортеж (By, value) для локатора
            timeout: Время ожидания в секундах
            
        Returns:
            bool: True если элемент видим, False иначе
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
