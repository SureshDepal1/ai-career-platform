from django.urls import path
from .views import CareerListView, CareerDetailView

urlpatterns = [
    path('careers/', CareerListView.as_view(), name='career-list'),
    path('careers/<int:pk>/', CareerDetailView.as_view(), name='career-detail'),
]