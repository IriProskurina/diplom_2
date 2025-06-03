import pytest
import allure
from utils.api import StellarBurgersAPI


@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с невалидными ингредиентами")
    def test_create_order_with_invalid_ingredients_fails(self, api_client):
        client, user_data = api_client

        # Регистрация и авторизация
        registration_data = {
            'email': user_data['email'],
            'password': user_data['password'],
            'name': user_data['name']
        }
        response_register = client.register_user(**registration_data)
        response_login = client.login_user(user_data['email'], user_data['password'])
        access_token = response_login.json().get('accessToken')
        client.token = access_token  # Присваиваем токен клиенту

        # Попытка создать заказ с невалидными ингредиентами
        invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
        response = client.create_order(ingredients=invalid_ingredients)
        assert response.status_code in [400, 403, 500], f"Ожидался код 400, 403 или 500, получен {response.status_code}"