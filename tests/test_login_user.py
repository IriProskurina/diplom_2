import pytest
import allure
from utils.api import StellarBurgersAPI
from data import user_data


@pytest.fixture
def api_client():
    client = StellarBurgersAPI()
    yield client, user_data
    # Удаление курьера после теста (если требуется)
    # client.delete_user(user_data['email'])


@allure.feature("Авторизация пользователя")
class TestLoginUser:
    @allure.story("Авторизация с некорректными данными")
    @pytest.mark.parametrize("email, password, expected_message", [
        ("wrong_" + user_data['email'], user_data['password'], "email or password are incorrect"),
        (user_data['email'], "wrong_" + user_data['password'], "email or password are incorrect"),
    ], ids=["wrong_email", "wrong_password"])
    @allure.title("Авторизация с неверными данными")
    def test_login_with_wrong_credentials(self, api_client, email, password, expected_message):
        """
        Негативный сценарий: авторизация с неверными данными.
        """
        client, _ = api_client
        response = client.login_user(email, password)
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == expected_message, "Неверное сообщение об ошибке"

    @allure.story("Авторизация с отсутствием данных")
    @pytest.mark.parametrize("email, password, expected_message", [
        ("", user_data['password'], "email or password are incorrect"),
        (user_data['email'], "", "email or password are incorrect"),
    ], ids=["no_email", "no_password"])
    @allure.title("Авторизация без указания данных")
    def test_login_without_credentials(self, api_client, email, password, expected_message):
        """
        Негативный сценарий: попытка авторизации без указания данных.
        """
        client, _ = api_client
        response = client.login_user(email, password)
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert response.json()["message"] == expected_message, "Неверное сообщение об ошибке"