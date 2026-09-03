from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
)
from .models import UserProfile


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile