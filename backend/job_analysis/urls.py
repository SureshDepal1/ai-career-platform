from django.urls import path

from .views import JobDescriptionCreateView


urlpatterns = [
    path(
        'job-descriptions/',
        JobDescriptionCreateView.as_view(),
        name='job-description-create'
    ),
]