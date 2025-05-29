from rest_framework import serializers
from .models import Bulletins


class BulletinsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bulletins
        fields = ('title', 'description', 'created_at')