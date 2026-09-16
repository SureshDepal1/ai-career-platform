from django.urls import path

from .views import (
    JobDescriptionCreateView,
    JobDescriptionAnalysisView,
)


urlpatterns = [

    path(
        'job-descriptions/',
        JobDescriptionCreateView.as_view(),
        name='job-description-create'
    ),

    path(
        'job-descriptions/<int:job_id>/analyze/',
        JobDescriptionAnalysisView.as_view(),
        name='job-description-analysis'
    ),

]
