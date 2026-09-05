from django.urls import path
from .views import CareerListView, CareerDetailView, SkillGapView


urlpatterns = [
    path('careers/', CareerListView.as_view(), name='career-list'),

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
]