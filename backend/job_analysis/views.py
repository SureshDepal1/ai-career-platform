from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import JobDescription
from .serializers import JobDescriptionSerializer


class JobDescriptionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobDescriptionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)