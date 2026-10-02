import json

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from careers.models import Career, Skill

from .models import AssessmentAttempt, AssessmentQuestion, InterviewSession, InterviewTurn
from .serializers import AssessmentAttemptSerializer, AssessmentQuestionSerializer, InterviewSessionSerializer
from .services import evaluate_interview_answer, generate_interview_question


class AssessmentOptionsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        careers = [{'id': item.id, 'title': item.title} for item in Career.objects.all()]
        skills = [{'id': item.id, 'name': item.name, 'category': item.category} for item in Skill.objects.all()]
        return Response({'careers': careers, 'skills': skills})


class AssessmentStartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        career = get_object_or_404(Career, id=request.data.get('career_id'))
        skill = get_object_or_404(Skill, id=request.data.get('skill_id'))
        question_count = min(max(int(request.data.get('question_count', 5)), 1), 10)
        questions = list(AssessmentQuestion.objects.filter(skill=skill).order_by('?')[:question_count])
        if not questions:
            return Response({'detail': 'No assessment questions are available for this skill yet.'}, status=status.HTTP_404_NOT_FOUND)
        attempt = AssessmentAttempt.objects.create(
            user=request.user,
            career=career,
            skill=skill,
            questions=[question.id for question in questions],
            total_questions=len(questions),
        )
        return Response({
            'attempt_id': attempt.id,
            'career': {'id': career.id, 'title': career.title},
            'skill': {'id': skill.id, 'name': skill.name},
            'questions': AssessmentQuestionSerializer(questions, many=True).data,
        }, status=status.HTTP_201_CREATED)


class AssessmentSubmitView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, attempt_id):
        attempt = get_object_or_404(AssessmentAttempt, id=attempt_id, user=request.user)
        submitted = {int(item['question_id']): int(item['selected_option']) for item in request.data.get('answers', [])}
        questions = AssessmentQuestion.objects.filter(id__in=attempt.questions)
        correct = sum(1 for question in questions if submitted.get(question.id) == question.correct_option)
        weak = [] if correct == attempt.total_questions else [attempt.skill.name]
        attempt.answers = [{'question_id': question.id, 'selected_option': submitted.get(question.id)} for question in questions]
        attempt.correct_answers = correct
        attempt.score_percentage = round(correct / attempt.total_questions * 100) if attempt.total_questions else 0
        attempt.weak_areas = weak
        attempt.recommended_skills = [attempt.skill.name] if weak else []
        attempt.save()
        return Response(AssessmentAttemptSerializer(attempt).data)


class AssessmentHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssessmentAttemptSerializer

    def get_queryset(self):
        return AssessmentAttempt.objects.filter(user=self.request.user)


class AssessmentResultView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssessmentAttemptSerializer

    def get_queryset(self):
        return AssessmentAttempt.objects.filter(user=self.request.user)


class InterviewStartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        career = get_object_or_404(Career, id=request.data.get('career_id'))
        difficulty = request.data.get('difficulty', 'medium')
        if difficulty not in dict(InterviewSession.DIFFICULTIES):
            return Response({'detail': 'Invalid interview difficulty.'}, status=status.HTTP_400_BAD_REQUEST)
        session = InterviewSession.objects.create(user=request.user, career=career, difficulty=difficulty)
        try:
            question = generate_interview_question(career, difficulty, 1)
        except (ValueError, json.JSONDecodeError) as exc:
            session.delete()
            return Response({'detail': f'Unable to generate an interview question: {exc}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as exc:
            session.delete()
            return Response({'detail': f'Interview AI is unavailable: {exc}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'session_id': session.id, 'question_number': 1, 'question': question}, status=status.HTTP_201_CREATED)


class InterviewAnswerView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user, status='active')
        question = request.data.get('question', '').strip()
        answer = request.data.get('answer', '').strip()
        if not question or not answer:
            return Response({'detail': 'Question and answer are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            evaluation = evaluate_interview_answer(session.career, session.difficulty, question, answer)
        except Exception as exc:
            return Response({'detail': f'Interview evaluation failed: {exc}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        number = session.turns.count() + 1
        InterviewTurn.objects.create(
            session=session,
            question_number=number,
            question=question,
            answer=answer,
            score=evaluation['score'],
            strengths=evaluation.get('strengths', []),
            weaknesses=evaluation.get('weaknesses', []),
            suggestions=evaluation.get('suggestions', []),
            better_answer=evaluation.get('better_answer', ''),
        )
        max_questions = 5
        if number >= max_questions:
            turns = list(session.turns.all())
            session.status = 'completed'
            session.overall_score = round(sum(turn.score for turn in turns) / len(turns))
            session.technical_score = session.overall_score
            session.communication_feedback = evaluation.get('communication_feedback', '')
            session.weak_skills = evaluation.get('technical_topics', [])
            session.preparation_topics = evaluation.get('suggestions', [])
            session.next_steps = ['Review your weakest answers.', 'Practice explaining technical decisions aloud.', 'Retake an interview at the next difficulty.']
            session.completed_at = timezone.now()
            session.save()
            return Response({'completed': True, 'evaluation': evaluation, 'result': InterviewSessionSerializer(session).data})
        try:
            next_question = generate_interview_question(session.career, session.difficulty, number + 1)
        except Exception as exc:
            return Response({'detail': f'Unable to generate the next interview question: {exc}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'completed': False, 'evaluation': evaluation, 'question_number': number + 1, 'question': next_question})


class InterviewHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSessionSerializer

    def get_queryset(self):
        return InterviewSession.objects.filter(user=self.request.user)


class InterviewResultView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSessionSerializer

    def get_queryset(self):
        return InterviewSession.objects.filter(user=self.request.user)
