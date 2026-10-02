from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class UserApiTests(APITestCase):
    def test_registration_creates_profile(self):
        response = self.client.post('/api/register/', {
            'username': 'new-user',
            'email': 'new@example.com',
            'password': 'safe-password-123',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='new-user').exists())
        self.assertTrue(hasattr(User.objects.get(username='new-user'), 'userprofile'))

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(username='existing', password='safe-password-123')

        response = self.client.post('/api/register/', {
            'username': 'existing',
            'email': 'new@example.com',
            'password': 'safe-password-123',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_requires_authentication_and_is_private(self):
        self.assertEqual(
            self.client.get('/api/profile/').status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        first = User.objects.create_user(username='first', password='safe-password-123')
        second = User.objects.create_user(username='second', password='safe-password-123')
        self.client.force_authenticate(first)
        self.client.put('/api/profile/', {'bio': 'private'}, format='json')
        self.client.force_authenticate(second)
        response = self.client.get('/api/profile/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['bio'], 'private')
