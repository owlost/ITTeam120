# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    # Test the User model to ensure user data is correctly stored and retrieved.
    def setUp(self):
        # Set up test case by creating a book instance.
        print("Setting up UserModelTest...")
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        print("User created successfully.")

    def test_user_creation(self):
        # Test if a user can be successfully created and attributes are correct.
        print("Running test_user_creation...")
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("password123"))
        print("OK - User creation test passed!")

    def test_user_str_method(self):
        # Test if the __str__ method of User returns the correct format.
        print("Running test_user_str_method...")
        self.assertEqual(str(self.user), "testuser (Student)")
        print("OK - __str__ method test passed!")


class UserLoginTest(TestCase):
    # Test user login functionality, including successful and failed login attempts.
    def setUp(self):
        # Set up test case by creating a user for login tests.
        print("Setting up UserLoginTest...")
        self.user = User.objects.create_user(username="loginuser", password="securepass")
        print("User created successfully.")

    def test_successful_login(self):
        # Test if a user can log in successfully with correct credentials.
        print("Running test_successful_login...")
        login = self.client.login(username="loginuser", password="securepass")
        print("OK - Login request completed.")
        self.assertTrue(login)
        print("OK - Successful login test passed!")

    def test_failed_login_with_wrong_password(self):
        # Test if login fails when incorrect credentials are provided."
        print("Running test_failed_login_with_wrong_password...")
        login = self.client.login(username="loginuser", password="wrongpass")
        print("OK - Login request completed.")
        self.assertFalse(login)
        print("OK - Failed login test passed!")
