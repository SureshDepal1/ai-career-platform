from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from careers.models import Skill, UserSkill
from .models import JobAnalysis, JobDescription


class JobAnalysisApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='candidate',
            password='safe-password-123',
        )
        self.other = User.objects.create_user(
            username='other',
            password='safe-password-123',
        )
        self.job = JobDescription.objects.create(
            user=self.user,
            title='Python Developer',
            description='Python and SQL experience required.',
        )
        self.python = Skill.objects.create(name='Python')
        UserSkill.objects.create(user=self.user, skill=self.python, proficiency=4)
        self.client.force_authenticate(self.user)

    def test_job_creation_is_authenticated_and_list_is_private(self):
        self.client.force_authenticate(None)
        self.assertEqual(
            self.client.post('/api/job-descriptions/create/', {}).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.get('/api/job-descriptions/').data[0]['id'], self.job.id)

    @patch('job_analysis.views.generate_career_analysis')
    def test_analysis_is_saved_and_reused(self, generate):
        generate.side_effect = [
            '```text\nPython | Programming | 5\npython | Programming | 4\nbad line\n```',
            'Focus on Python practice.',
        ]

        response = self.client.get(f'/api/job-descriptions/{self.job.id}/analyze/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(JobAnalysis.objects.count(), 1)
        self.assertEqual(len(response.data['analysis']['required_skills']), 1)
        self.client.get(f'/api/job-descriptions/{self.job.id}/analyze/')
        self.assertEqual(generate.call_count, 2)

    def test_other_user_cannot_analyze_or_retrieve_job(self):
        other_job = JobDescription.objects.create(
            user=self.other,
            title='Private',
            description='Private description',
        )
        self.assertEqual(
            self.client.get(f'/api/job-descriptions/{other_job.id}/analyze/').status_code,
            status.HTTP_404_NOT_FOUND,
        )
