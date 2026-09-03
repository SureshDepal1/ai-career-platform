from rest_framework import generics
from .models import Career
from .serializers import CareerSerializer


class CareerListView(generics.ListAPIView):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer


class CareerDetailView(generics.RetrieveAPIView):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer