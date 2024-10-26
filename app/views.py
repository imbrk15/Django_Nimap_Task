from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, ProjectViewSerializer


class ClientListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectCreateView(APIView):
    def post(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response(
                {"client": ["Client with this ID does not exist."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = request.data
        data["client"] = client.id

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(users=request.user)
        serializer = ProjectViewSerializer(projects, many=True)
        return Response(serializer.data)
