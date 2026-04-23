from courses.models import Course
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project

User = get_user_model()


class ProjectModelUnitTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="projects.admin@example.com",
            password="StrongPass123!",
            user_type="admin",
        )
        self.course = Course.objects.create(
            title="Project Metrics Path",
            description="A valid course used to verify project counters and ordering logic.",
            level="beginner",
            category="web",
            estimated_duration=10,
            is_public=True,
            instructor=self.admin,
        )

    def test_creating_project_updates_course_projects_count(self):
        Project.objects.create(
            course=self.course,
            title="First Project",
            description="A detailed project description that is long enough to be valid.",
            requirements="Install tooling",
            objectives="Practice testing",
            resources="Docs",
            estimated_time=5,
            level="beginner",
            language="python",
        )

        self.course.refresh_from_db()
        self.assertEqual(self.course.projects_count, 1)
        self.assertEqual(self.course.get_actual_projects_count(), 1)


class ProjectApiIntegrationTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="projects.api.admin@example.com",
            password="StrongPass123!",
            user_type="admin",
        )
        self.learner = User.objects.create_user(
            email="projects.api.learner@example.com",
            password="StrongPass123!",
            user_type="learner",
        )
        self.course = Course.objects.create(
            title="Learner Delivery Path",
            description="A valid course used for end-to-end project API integration coverage.",
            level="advanced",
            category="ai",
            estimated_duration=20,
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

    def test_admin_can_create_project_and_list_by_course(self):
        self.authenticate(self.admin)

        create_response = self.client.post(
            reverse("projects:create-project"),
            {
                "course_id": self.course.id,
                "title": "Capstone API Project",
                "description": "A sufficiently detailed project description for integration testing.",
                "requirements": "Python and Django",
                "objectives": "Ship a real feature",
                "resources": "API docs",
                "estimated_time": 8,
                "level": "intermediate",
                "language": "python",
                "order": 1,
            },
            format="json",
        )
        list_response = self.client.get(
            reverse("projects:course-projects", kwargs={"course_id": self.course.id})
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(create_response.data["success"])
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["count"], 1)
        self.assertEqual(
            list_response.data["projects"][0]["title"], "Capstone API Project"
        )

    def test_learner_can_start_project_only_after_joining_course(self):
        project = Project.objects.create(
            course=self.course,
            title="Startable Project",
            description="A sufficiently detailed project description for start flow coverage.",
            requirements="Join the course first",
            objectives="Verify access rules",
            resources="Project brief",
            estimated_time=6,
            level="beginner",
            language="javascript",
        )
        self.authenticate(self.learner)

        denied_response = self.client.post(
            reverse("projects:start-project", kwargs={"pk": project.id}),
            {},
            format="json",
        )
        self.client.post(
            reverse("courses:join-course", kwargs={"id": self.course.id}),
            {},
            format="json",
        )
        allowed_response = self.client.post(
            reverse("projects:start-project", kwargs={"pk": project.id}),
            {},
            format="json",
        )

        self.assertEqual(denied_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(allowed_response.status_code, status.HTTP_200_OK)
        self.assertTrue(allowed_response.data["success"])
