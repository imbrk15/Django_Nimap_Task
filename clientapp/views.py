# clientapp/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, ClientDetailSerializer, UserSerializer

# List all clients


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_clients(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

# Register a new client


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_client(request):
    data = request.data.copy()
    # Assign the logged-in user as created_by
    data['created_by'] = request.user.id
    serializer = ClientSerializer(data=data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve a client and its projects


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientDetailSerializer(client)
    return Response(serializer.data)

# Update client info


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a client


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    client.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Create a new project for a client and assign users


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request, client_id):
    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    project = Project(name=data['project_name'],
                      client=client, created_by=request.user)
    project.save()

    user_ids = [user['id'] for user in data.get('users', [])]
    users = User.objects.filter(id__in=user_ids)
    project.users.set(users)

    serializer = ProjectSerializer(project)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# List projects assigned to the logged-in user


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_projects(request):
    projects = request.user.assigned_projects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)
