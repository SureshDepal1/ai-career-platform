from django.urls import path

from .views import (
    AssessmentHistoryView,
    AssessmentOptionsView,
    AssessmentResultView,
    AssessmentStartView,
    AssessmentSubmitView,
    InterviewAnswerView,
    InterviewHistoryView,
    InterviewResultView,
    InterviewStartView,
)

urlpatterns = [
    path('assessments/options/', AssessmentOptionsView.as_view()),
    path('assessments/start/', AssessmentStartView.as_view()),
    path('assessments/<int:attempt_id>/submit/', AssessmentSubmitView.as_view()),
    path('assessments/history/', AssessmentHistoryView.as_view()),
    path('assessments/<int:pk>/', AssessmentResultView.as_view()),
    path('interviews/start/', InterviewStartView.as_view()),
    path('interviews/<int:session_id>/answer/', InterviewAnswerView.as_view()),
    path('interviews/history/', InterviewHistoryView.as_view()),
    path('interviews/<int:pk>/', InterviewResultView.as_view()),
]
