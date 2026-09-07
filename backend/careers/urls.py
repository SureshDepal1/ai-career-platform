from django.urls import path
from .views import (
    CareerListView,
    CareerDetailView,
    SkillGapView,
    RoadmapView,
    RecommendationView,
    ReadinessScoreView,
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
]