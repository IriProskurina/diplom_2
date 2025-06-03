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


@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.title("Создание заказа без ингредиентов (авторизованный)")
    def test_empty_ingredients_authenticated(self, api_client):
        """Тест создания заказа без ингредиентов с авторизацией"""
        client, user_data = api_client

        with allure.step("Регистрация пользователя"):
            client.register_user(
                email=user_data['email'],
                password=user_data['password'],
                name=user_data['name']
            )

        with allure.step("Авторизация пользователя"):
            client.login_user(
                email=user_data['email'],
                password=user_data['password']
            )

        with allure.step("Создание заказа без ингредиентов"):
            response = client.create_order(ingredients=[])

        # Здесь API возвращает 400, значит допускаем его
        assert response.status_code == 400, (
            f"Ожидался код 400, получен {response.status_code}"
        )