import pytest
import allure
from utils.api import StellarBurgersAPI


@allure.feature("Авторизация пользователя")
class TestLoginUser:
    @allure.story("Авторизация существующего пользователя")
    @allure.title("Успешная авторизация пользователя с правильными данными")
    def test_login_existing_user_success(self, api_client):
        """
        Позитивный сценарий: успешная авторизация с действующими учетными данными.
        """
        client, data = api_client
        # Убираем ненужный ключ 'created_user' перед регистрацией
        clean_data = {k: v for k, v in data.items() if k != 'created_user'}
        client.register_user(**clean_data)
        data['created_user'] = True  # Восстанавливаем ключ, если нужно для других тестов

        # Осуществляем авторизацию
        response = client.login_user(data['email'], data['password'])
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert "accessToken" in response.json(), "В ответе отсутствует accessToken"

    @allure.story("Авторизация с некорректными данными")
    @allure.title("Авторизация с неверным email")
    def test_login_with_wrong_email_fails(self, api_client):
        """
        Негативный сценарий: авторизация с неверным email.
        """
        client, data = api_client
        response = client.login_user("wrong_" + data['email'], data['password'])
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.story("Авторизация с некорректными данными")
    @allure.title("Авторизация с неверным паролем")
    def test_login_with_wrong_password_fails(self, api_client):
        """
        Негативный сценарий: авторизация с неверным паролем.
        """
        client, data = api_client
        response = client.login_user(data['email'], "wrong_" + data['password'])
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.story("Авторизация с отсутствием данных")
    @allure.title("Авторизация без указания email")
    def test_login_without_email_fails(self, api_client):
        """
        Негативный сценарий: попытка авторизации без указания email.
        """
        client, data = api_client
        response = client.login_user("", data['password'])
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.story("Авторизация с отсутствием данных")
    @allure.title("Авторизация без указания пароля")
    def test_login_without_password_fails(self, api_client):
        """
        Негативный сценарий: попытка авторизации без указания пароля.
        """
        client, data = api_client
        response = client.login_user(data['email'], "")
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.story("Авторизация пользователя с особым почтовым адресом")
    @allure.title("Авторизация с кириллическим email")
    def test_login_with_cyrillic_email_fails(self, api_client):
        """
        Негативный сценарий: авторизация с кириллической почтой.
        """
        client, data = api_client
        cyrillic_email = "пользователь@mail.ru"
        response = client.login_user(cyrillic_email, data['password'])
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.story("Авторизация пользователя с особенными значениями")
    @allure.title("Авторизация с длинной почтой")
    def test_login_with_long_email_fails(self, api_client):
        """
        Граница: проверка максимального размера электронного адреса.
        """
        client, data = api_client
        long_email = "a" * 255 + "@mail.ru"
        response = client.login_user(long_email, data['password'])
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.story("Авторизация пользователя с особыми символами")
    @allure.title("Авторизация с электронным адресом, содержащим спецсимволы")
    def test_login_with_special_characters_email_fails(self, api_client):
        """
        Граница: проверка поведения при специальной форме почтового адреса.
        """
        client, data = api_client
        special_email = "!#$%^&*()+=-_.~'@mail.ru"
        response = client.login_user(special_email, data['password'])
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.story("Авторизация пользователя с долгим паролем")
    @allure.title("Авторизация с длинным паролем")
    def test_login_with_long_password_fails(self, api_client):
        """
        Граница: проверка реакции на очень длинный пароль.
        """
        client, data = api_client
        long_password = "a" * 129
        response = client.login_user(data['email'], long_password)
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.story("Авторизация пользователя с численным идентификатором")
    @allure.title("Авторизация с цифровым паролем")
    def test_login_with_numeric_password(self, api_client):
        """
        Спецслучай: проверка поведения при цифровом пароле.
        """
        client, data = api_client
        numeric_password = "12345678"
