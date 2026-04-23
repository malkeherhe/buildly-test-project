from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course

User = get_user_model()


class CourseModelUnitTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="courses.admin@example.com",
            password="StrongPass123!",
            user_type="admin",
        )
        self.learner = User.objects.create_user(
            email="courses.learner@example.com",
            password="StrongPass123!",
            user_type="learner",
        )
        self.course = Course.objects.create(
            title="API Testing Path",
            description="A detailed learning path for testing backend APIs well.",
            level="beginner",
            category="web",
            estimated_duration=12,
            is_public=True,
            instructor=self.admin,
        )

    def test_add_and_remove_learner_updates_user_snapshot(self):
        added = self.course.add_learner(self.learner)
        self.learner.refresh_from_db()

        self.assertTrue(added)
        self.assertTrue(self.course.is_student_enrolled(self.learner))
        self.assertIn(self.course.title, self.learner.get_enrolled_courses_list())

        removed = self.course.remove_learner(self.learner)
        self.learner.refresh_from_db()

        self.assertTrue(removed)
        self.assertFalse(self.course.is_student_enrolled(self.learner))
        self.assertNotIn(self.course.title, self.learner.get_enrolled_courses_list())


class CourseApiIntegrationTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="courses.api.admin@example.com",
            password="StrongPass123!",
            user_type="admin",
        )
        self.learner = User.objects.create_user(
            email="courses.api.learner@example.com",
            password="StrongPass123!",
            user_type="learner",
        )
        self.course = Course.objects.create(
            title="Integration Testing Path",
            description="A detailed learning path for exercising real API interactions.",
            level="intermediate",
            category="ai",
            estimated_duration=18,
            is_public=True,
            instructor=self.admin,
        )

    def authenticate(self, user):
        response = self.client.post(
            reverse("login"),
            {
                "email": user.email,
                "password": "StrongPass123!",
            },
            format="json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['tokens']['access']}"
        )

    def test_admin_can_create_course(self):
        self.authenticate(self.admin)

        response = self.client.post(
            reverse("courses:create-course"),
            {
                "title": "Performance Engineering Path",
                "description": "A long enough description for creating a valid course record.",
                "level": "advanced",
                "category": "data",
                "estimated_duration": 24,
                "is_public": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(
            response.data["course"]["title"], "Performance Engineering Path"
        )

    def test_learner_can_join_course_and_see_it_in_my_courses(self):
        self.authenticate(self.learner)

        join_response = self.client.post(
            reverse("courses:join-course", kwargs={"id": self.course.id}),
            {},
            format="json",
        )
        my_courses_response = self.client.get(reverse("courses:my-courses"))

        self.assertEqual(join_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(join_response.data["success"])
        self.assertEqual(my_courses_response.status_code, status.HTTP_200_OK)
        self.assertEqual(my_courses_response.data["count"], 1)
        self.assertEqual(
            my_courses_response.data["courses"][0]["title"], self.course.title
        )

    def test_learner_cannot_join_same_course_twice(self):
        self.authenticate(self.learner)
        first_response = self.client.post(
            reverse("courses:join-course", kwargs={"id": self.course.id}),
            {},
            format="json",
        )
        second_response = self.client.post(
            reverse("courses:join-course", kwargs={"id": self.course.id}),
            {},
            format="json",
        )

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(second_response.data["success"])
