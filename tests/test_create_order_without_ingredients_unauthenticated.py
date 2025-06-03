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
    @allure.title("Создание заказа без ингредиентов (неавторизованный)")
    def test_empty_ingredients_unauthenticated(self, api_client):
        """Тест создания заказа без ингредиентов без авторизации"""
        client, _ = api_client

        with allure.step("Создание заказа без ингредиентов"):
            response = client.create_order(ingredients=[])

        # Оставляем прежнюю логику, так как API возвращает 400
        assert response.status_code == 400, (
            f"Ожидался код 400, получен {response.status_code}"
        )