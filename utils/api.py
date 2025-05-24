import requests


class StellarBurgersAPI:
    BASE_URL = "https://spaceburger.galaxy.net/api"

    def __init__(self):
        self.session = requests.Session()
        self.access_token = None

    def signup_user(self, email, password, username):
        """Регистрация нового пользователя."""
        endpoint = f"{self.BASE_URL}/users/sign-up"
        payload = {
            "email": email,
            "password": password,
            "username": username
        }
        return self.session.post(endpoint, json=payload)

    def authenticate_user(self, email, password):
        """Авторизоваться в системе."""
        endpoint = f"{self.BASE_URL}/users/authenticate"
        payload = {
            "email": email,
            "password": password
        }
        response = self.session.post(endpoint, json=payload)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get("token")
        return response

    def remove_user_account(self):
        """Удалить аккаунт пользователя."""
        endpoint = f"{self.BASE_URL}/users/delete"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        return self.session.delete(endpoint, headers=headers)

    def modify_user_profile(self, new_email=None, new_password=None, new_username=None):
        """Обновить профиль пользователя."""
        endpoint = f"{self.BASE_URL}/users/profile/update"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        payload = {}
        if new_email is not None:
            payload["email"] = new_email
        if new_password is not None:
            payload["password"] = new_password
        if new_username is not None:
            payload["username"] = new_username
        return self.session.put(endpoint, headers=headers, json=payload)

    def place_order(self, items, include_token=True):
        """Оформить заказ на продукты."""
        endpoint = f"{self.BASE_URL}/orders/create"
        headers = {"Authorization": f"Bearer {self.access_token}"} if include_token and self.access_token else {}
        payload = {"items": items}
        return self.session.post(endpoint, headers=headers, json=payload)

    def fetch_orders(self, include_token=True):
        """Получить историю заказов пользователя."""
        endpoint = f"{self.BASE_URL}/orders/history"
        headers = {"Authorization": f"Bearer {self.access_token}"} if include_token and self.access_token else {}
        return self.session.get(endpoint, headers=headers)