from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class CustomUserUnitTests(APITestCase):
    def test_learner_enrollment_helpers_track_titles(self):
        learner = User.objects.create_user(
            email="learner.helpers@example.com",
            password="StrongPass123!",
            user_type="learner",
        )

        added = learner.add_enrolled_course("Testing Path")
        learner.refresh_from_db()

        self.assertTrue(added)
        self.assertEqual(learner.get_enrolled_courses_count(), 1)
        self.assertIn("Testing Path", learner.get_enrolled_courses_list())

        removed = learner.remove_enrolled_course("Testing Path")
        learner.refresh_from_db()

        self.assertTrue(removed)
        self.assertEqual(learner.get_enrolled_courses_count(), 0)

    def test_admin_save_clears_enrollment_titles(self):
        admin = User.objects.create_user(
            email="admin.helpers@example.com",
            password="StrongPass123!",
            user_type="admin",
            enrolled_courses_titles=["Should be cleared"],
        )

        admin.refresh_from_db()

        self.assertIsNone(admin.enrolled_courses_titles)


class AccountApiIntegrationTests(APITestCase):
    def test_register_learner_returns_tokens_and_learner_profile(self):
        response = self.client.post(
            reverse("register-learner"),
            {
                "email": "learner.api@example.com",
                "password": "StrongPass123!",
                "password2": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", response.data)
        self.assertEqual(response.data["user"]["email"], "learner.api@example.com")
        self.assertEqual(response.data["user"]["enrolled_courses_count"], 0)

    def test_login_and_profile_flow(self):
        user = User.objects.create_user(
            email="login.flow@example.com",
            password="StrongPass123!",
            user_type="learner",
        )

        login_response = self.client.post(
            reverse("login"),
            {
                "email": user.email,
                "password": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        profile_response = self.client.get(reverse("profile"))

        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["user"]["email"], user.email)

    def test_logout_requires_refresh_token(self):
        user = User.objects.create_user(
            email="logout.flow@example.com",
            password="StrongPass123!",
            user_type="learner",
        )
        login_response = self.client.post(
            reverse("login"),
            {
                "email": user.email,
                "password": "StrongPass123!",
            },
            format="json",
        )
        access_token = login_response.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        logout_response = self.client.post(reverse("logout"), {}, format="json")

        self.assertEqual(logout_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", logout_response.data)
