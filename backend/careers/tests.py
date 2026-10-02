from django.contrib.auth.models import User
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Career, CareerSkill, Skill, UserSkill


class CareerApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='learner',
            password='safe-password-123',
        )
        self.career = Career.objects.create(title='Backend Developer')
        self.python = Skill.objects.create(name='Python', category='Programming')
        self.sql = Skill.objects.create(name='SQL', category='Database')
        CareerSkill.objects.create(career=self.career, skill=self.python, importance=4)
        CareerSkill.objects.create(career=self.career, skill=self.sql, importance=3)
        self.client.force_authenticate(self.user)

    def test_career_list_and_detail_work(self):
        self.assertEqual(self.client.get('/api/careers/').status_code, status.HTTP_200_OK)
        response = self.client.get(f'/api/careers/{self.career.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Backend Developer')

    def test_skill_gap_has_no_implicit_ai_call(self):
        UserSkill.objects.create(user=self.user, skill=self.python, proficiency=4)

        response = self.client.get(f'/api/careers/{self.career.id}/skill-gap/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('ai_analysis', response.data)
        self.assertEqual(response.data['skill_gaps'][0]['status'], 'Good')
        self.assertEqual(response.data['skill_gaps'][1]['status'], 'Missing')

    def test_structured_skills_are_owned_and_validated(self):
        response = self.client.post('/api/skills/', {
            'skill_id': self.python.id,
            'proficiency': 6,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post('/api/skills/', {
            'skill_id': self.python.id,
            'proficiency': 4,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.client.get('/api/skills/').data[0]['proficiency'], 4)

    def test_readiness_score_is_skill_coverage(self):
        UserSkill.objects.create(user=self.user, skill=self.python, proficiency=2)

        response = self.client.get(f'/api/careers/{self.career.id}/readiness-score/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['readiness_score'], 29)

    @patch('careers.views.generate_career_analysis', return_value='Practice Python projects first.')
    def test_ai_analysis_requires_explicit_action(self, generate):
        response = self.client.post(f'/api/careers/{self.career.id}/ai-analysis/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ai_analysis'], 'Practice Python projects first.')
        generate.assert_called_once()
