from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserTokenTest(APITestCase):

    def test_create_user_and_get_token(self):
        """
        Убедимся, что мы можем создать нового пользователя
        и получить для него токен.

        """
        create_url = reverse('users-list')
        user_data = {
            "email": "designer@example.com",
            "first_name": "Dave",
            "last_name": "Simonov",
            "password": "God2024Ura!",
            "is_customer": False
        }
        create_response = self.client.post(
            create_url,
            user_data,
            format='json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        print('Пользователь успешно создан.')

        for field in user_data:
            if field != 'password':
                self.assertEqual(create_response.data[field], user_data[field])
        print('Данные пользователя верифицированы.')

        token_url = reverse('login')
        token_data = {
            "email": user_data['email'],
            "password": user_data['password']
        }
        token_response = self.client.post(token_url, token_data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)

        self.assertIn('auth_token', token_response.data)
        print('Токен успешно получен.')
