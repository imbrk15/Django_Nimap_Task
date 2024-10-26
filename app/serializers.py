from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project
from django.core.exceptions import ObjectDoesNotExist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Client
        fields = ["id", "client_name", "created_at", "created_by"]


class ProjectViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "project_name",
            "created_at",
            "created_by",
        )


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    user_data = serializers.ListField(write_only=True)
    created_by = serializers.CharField(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "project_name",
            "client",
            "users",
            "user_data",
            "created_at",
            "created_by",
        )

    def to_representation(self, instance):
        """Customize the output representation of the Project instance."""
        representation = super().to_representation(instance)

        representation["client"] = (
            instance.client.client_name if instance.client else None
        )

        return representation

    def validate_user_data(self, value):
        """Validate that each user dictionary has an 'id' and 'name'."""
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "User data must be a list of user objects."
            )

        user_ids = []
        for user in value:
            if not isinstance(user, dict):
                raise serializers.ValidationError(
                    "Each user entry must be a dictionary with 'id' and 'name' fields."
                )
            if "id" not in user or "name" not in user:
                raise serializers.ValidationError(
                    "Each user must contain 'id' and 'name'."
                )
            if not isinstance(user["id"], int):
                raise serializers.ValidationError(
                    "The 'id' field must be an integer.")
            if not isinstance(user["name"], str):
                raise serializers.ValidationError(
                    "The 'name' field must be a string.")

            user_ids.append(user["id"])

        existing_users = User.objects.filter(id__in=user_ids).values_list(
            "id", flat=True
        )
        for user_id in user_ids:
            if user_id not in existing_users:
                raise serializers.ValidationError(
                    f"User with id {user_id} does not exist."
                )

        return value

    def create(self, validated_data):
        user_data = validated_data.pop("user_data")
        user_ids = [user["id"] for user in user_data]
        project = Project.objects.create(**validated_data)
        project.users.set(user_ids)
        return project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
