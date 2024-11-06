from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .utils import generate_email_verification_token  
class AuthAPITests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password")
        self.token = generate_email_verification_token(self.user)  # Assuming you have a token generator
        self.verify_email_url = reverse('verify-email') + f'?token={self.token}'

    def test_email_verification(self):
        # Test that the email verification URL works
        response = self.client.get(self.verify_email_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Email verified successfully!")

    def test_invalid_email_verification(self):
        # Test an invalid token
        invalid_token = "some_invalid_token"
        response = self.client.get(reverse('verify-email') + f'?token={invalid_token}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], "Invalid or expired token.")

    def test_signup_creates_user_and_returns_verification_url(self):
        # Test that user creation returns a verification URL
        response = self.client.post(reverse('signup'), {
            "username": "newuser",
            "password": "password123",
            "email": "newuser@example.com",
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("verification_url", response.json())

