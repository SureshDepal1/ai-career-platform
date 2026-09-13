from rest_framework import serializers

from .models import JobDescription


class JobDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobDescription
        fields = [
            'id',
            'title',
            'company',
            'description',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]