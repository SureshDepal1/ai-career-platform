from django.urls import path
from .views import (
    CareerListView,
    CareerDetailView,
    SkillGapView,
    RoadmapView,
    RecommendationView,
    ReadinessScoreView,
    CareerAIAnalysisView,
    UserSkillListCreateView,
    UserSkillDetailView,
)


urlpatterns = [
    path(
        'careers/',
        CareerListView.as_view(),
        name='career-list'
    ),

    path(
        'careers/<int:pk>/',
        CareerDetailView.as_view(),
        name='career-detail'
    ),

    path(
        'careers/<int:career_id>/skill-gap/',
        SkillGapView.as_view(),
        name='skill-gap'
    ),

    path(
        'careers/<int:career_id>/roadmap/',
        RoadmapView.as_view(),
        name='roadmap'
    ),

    path(
        'careers/<int:career_id>/recommendations/',
        RecommendationView.as_view(),
        name='recommendations'
    ),
    path(
    'careers/<int:career_id>/readiness-score/',
    ReadinessScoreView.as_view(),
    name='readiness-score'
    ),
    path(
        'careers/<int:career_id>/ai-analysis/',
        CareerAIAnalysisView.as_view(),
        name='career-ai-analysis',
    ),
    path('skills/', UserSkillListCreateView.as_view(), name='user-skill-list'),
    path('skills/<int:pk>/', UserSkillDetailView.as_view(), name='user-skill-detail'),
]