from django.urls import path

from .views import (
    JobDescriptionCreateView,
    JobDescriptionListView,
    JobDescriptionAnalysisView,
    SavedJobAnalysisView,
)


urlpatterns = [

    path(
        'job-descriptions/',
        JobDescriptionListView.as_view(),
        name='job-description-list'
    ),

    path(
        'job-descriptions/create/',
        JobDescriptionCreateView.as_view(),
        name='job-description-create'
    ),

    path(
        'job-descriptions/<int:job_id>/analyze/',
        JobDescriptionAnalysisView.as_view(),
        name='job-description-analysis'
    ),

    path(
        'job-analyses/<int:pk>/',
        SavedJobAnalysisView.as_view(),
        name='saved-job-analysis'
    ),

]