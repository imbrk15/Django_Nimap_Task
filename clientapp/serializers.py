# clientapp/serializers.py
from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(
        source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'created_at', 'created_by', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.name', read_only=True)
    users = UserSerializer(many=True, read_only=True)
    created_by = serializers.CharField(
        source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'client', 'users', 'created_at', 'created_by']


class ClientDetailSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    created_by = serializers.CharField(
        source='created_by.username', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'created_at',
                  'created_by', 'updated_at', 'projects']
