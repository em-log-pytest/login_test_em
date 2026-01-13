from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object для страницы логина saucedemo.com."""
    
    # Локаторы
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        """
        Инициализация страницы логина.
        
        Args:
            driver: Экземпляр WebDriver
        """
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/"
    
    def open(self):
        """
        Открытие страницы логина.
        """
        self.driver.get(self.url)
    
    def enter_username(self, username):
        """
        Ввод имени пользователя.
        
        Args:
            username: Имя пользователя для ввода
        """
        self.send_keys(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """
        Ввод пароля.
        
        Args:
            password: Пароль для ввода
        """
        self.send_keys(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """
        Клик по кнопке логина.
        """
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """
        Выполнение полного процесса логина.
        
        Args:
            username: Имя пользователя
            password: Пароль
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def get_error_message(self):
        """
        Получение текста сообщения об ошибке.
        
        Returns:
            str: Текст сообщения об ошибке или пустая строка, если сообщение не найдено
        """
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
