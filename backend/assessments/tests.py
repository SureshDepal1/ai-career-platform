from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from careers.models import Career, Skill
from .models import AssessmentAttempt, AssessmentQuestion


class AssessmentApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='student',
            password='safe-password-123',
        )
        self.other = User.objects.create_user(
            username='other-student',
            password='safe-password-123',
        )
        self.career = Career.objects.create(title='Developer')
        self.skill = Skill.objects.create(name='Python')
        self.question = AssessmentQuestion.objects.create(
            skill=self.skill,
            question='What is Python?',
            options=['A language', 'A database'],
            correct_option=0,
        )
        self.client.force_authenticate(self.user)

    def test_invalid_question_count_is_clean_400(self):
        response = self.client.post('/api/assessments/start/', {
            'career_id': self.career.id,
            'skill_id': self.skill.id,
            'question_count': 'abc',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('question_count', response.data)

    def test_assessment_can_be_started_submitted_and_is_private(self):
        response = self.client.post('/api/assessments/start/', {
            'career_id': self.career.id,
            'skill_id': self.skill.id,
            'question_count': 1,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        attempt_id = response.data['attempt_id']
        response = self.client.post(f'/api/assessments/{attempt_id}/submit/', {
            'answers': [{'question_id': self.question.id, 'selected_option': 0}],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['score_percentage'], 100)
        self.client.force_authenticate(self.other)
        self.assertEqual(
            self.client.get(f'/api/assessments/{attempt_id}/').status_code,
            status.HTTP_404_NOT_FOUND,
        )
