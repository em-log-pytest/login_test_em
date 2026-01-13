import pytest
import allure
from pages.login_page import LoginPage


@allure.feature("Login")
class TestLogin:
    """Тесты для функциональности логина на saucedemo.com."""
    
    @allure.story("Успешный логин")
    @allure.step("Открытие страницы логина")
    def test_successful_login(self, driver):
        """
        Тест успешного логина с валидными учетными данными.
        Проверяет переход на страницу инвентаря после логина.
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        with allure.step("Проверка видимости элементов формы логина"):
            assert login_page.is_element_visible(login_page.USERNAME_INPUT)
            assert login_page.is_element_visible(login_page.PASSWORD_INPUT)
            assert login_page.is_element_visible(login_page.LOGIN_BUTTON)
        
        with allure.step("Выполнение логина с валидными учетными данными (standard_user / secret_sauce)"):
            login_page.login("standard_user", "secret_sauce")
        
        with allure.step("Проверка URL после успешного логина"):
            assert "/inventory.html" in driver.current_url
    
    @allure.story("Неуспешный логин")
    @allure.step("Открытие страницы логина")
    def test_login_with_invalid_password(self, driver):
        """
        Тест логина с неверным паролем.
        Проверяет отображение сообщения об ошибке и остаток на странице логина.
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        with allure.step("Выполнение логина с неверным password"):
            login_page.login("standard_user", "wrong_password")
        
        with allure.step("Проверка URL - должен остаться на странице логина"):
            assert driver.current_url == "https://www.saucedemo.com/"
        
        with allure.step("Проверка видимости сообщения об ошибке"):
            assert login_page.is_element_visible(login_page.ERROR_MESSAGE)
        
        with allure.step("Проверка текста сообщения об ошибке"):
            error_text = login_page.get_error_message()
            assert "Username and password do not match" in error_text or "Epic sadface" in error_text
    
    @allure.story("Неуспешный логин")
    @allure.step("Открытие страницы логина")
    def test_login_locked_out_user(self, driver):
        """
        Тест логина заблокированного пользователя (locked_out_user).
        Проверяет отображение сообщения об ошибке и остаток на странице логина.
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        with allure.step("Выполнение логина заблокированным пользователем (locked_out_user)"):
            login_page.login("locked_out_user", "secret_sauce")
        
        with allure.step("Проверка URL - должен остаться на странице логина"):
            assert driver.current_url == "https://www.saucedemo.com/"
        
        with allure.step("Проверка видимости сообщения об ошибке"):
            assert login_page.is_element_visible(login_page.ERROR_MESSAGE)
        
        with allure.step("Проверка текста сообщения об ошибке"):
            error_text = login_page.get_error_message()
            assert "Sorry, this user has been locked out" in error_text or "Epic sadface" in error_text
    
    @allure.story("Неуспешный логин")
    @allure.step("Открытие страницы логина")
    def test_login_with_empty_fields(self, driver):
        """
        Тест логина с пустыми полями (username и password).
        Проверяет отображение сообщения об ошибке и остаток на странице логина.
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        with allure.step("Выполнение логина с пустыми полями"):
            login_page.login("", "")
        
        with allure.step("Проверка URL - должен остаться на странице логина"):
            assert driver.current_url == "https://www.saucedemo.com/"
        
        with allure.step("Проверка видимости сообщения об ошибке"):
            assert login_page.is_element_visible(login_page.ERROR_MESSAGE)
        
        with allure.step("Проверка текста сообщения об ошибке"):
            error_text = login_page.get_error_message()
            assert "Username is required" in error_text or "Epic sadface" in error_text
    
    @allure.story("Успешный логин")
    @allure.step("Открытие страницы логина")
    def test_login_performance_glitch_user(self, driver):
        """
        Тест логина пользователем performance_glitch_user.
        Проверяет корректный переход на страницу инвентаря и что страница открывается
        несмотря на возможные задержки.
        """
        login_page = LoginPage(driver)
        login_page.open()
        
        with allure.step("Проверка видимости элементов формы логина"):
            assert login_page.is_element_visible(login_page.USERNAME_INPUT)
            assert login_page.is_element_visible(login_page.PASSWORD_INPUT)
            assert login_page.is_element_visible(login_page.LOGIN_BUTTON)
        
        with allure.step("Выполнение логина пользователем performance_glitch_user"):
            login_page.login("performance_glitch_user", "secret_sauce")
        
        with allure.step("Проверка URL после успешного логина (с учетом возможных задержек)"):
            assert "/inventory.html" in driver.current_url
        
        with allure.step("Проверка, что страница инвентаря открылась корректно"):
            # Проверяем, что мы действительно на странице инвентаря, а не на странице логина
            assert driver.current_url != "https://www.saucedemo.com/"
            assert "/inventory.html" in driver.current_url
