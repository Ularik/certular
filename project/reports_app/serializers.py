from rest_framework import serializers
from .models import Reports
from accounts_app.models import Organization, User


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'patronymic')


class ReportsListSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    user = UserSerializer()

    class Meta:
        model = Reports
        fields = '__all__'