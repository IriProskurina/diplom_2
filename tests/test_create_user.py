from utils.api import StellarBurgersAPI
import allure
import pytest

class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, api_client):
        client, data = api_client
        # Убираем лишний ключ created_user
        del data['created_user']
        response = client.register_user(data['email'], data['password'], data['name'])  # Используется метод register_user
        assert response.status_code == 200 or response.status_code == 201

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user_fails(self, api_client):
        client, data = api_client
        # Удаляем созданный ранее ключ
        del data['created_user']
        # Первым делом регистрируем пользователя
        first_response = client.register_user(data['email'], data['password'], data['name'])
        assert first_response.status_code == 200 or first_response.status_code == 201

        # Повторная регистрация должна давать ошибку
        second_response = client.register_user(data['email'], data['password'], data['name'])
        assert second_response.status_code == 400

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field_fails(self, api_client, missing_field):
        client, data = api_client
        # Удаляем ненужный ключ created_user
        del data['created_user']
        user_data = data.copy()
        del user_data[missing_field]
        response = client.register_user(user_data.get('email'), user_data.get('password'), user_data.get('name'))
        assert response.status_code == 400