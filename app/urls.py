from django.urls import path
from .views import (
    ClientListCreateAPIView,
    ClientRetrieveUpdateDeleteAPIView,
    ProjectCreateView,
    UserProjectsAPIView,
)

urlpatterns = [
    path("clients/", ClientListCreateAPIView.as_view(), name="client-list-create"),
    path(
        "clients/<int:pk>/",
        ClientRetrieveUpdateDeleteAPIView.as_view(),
        name="client-detail",
    ),
    path(
        "clients/<int:client_id>/projects/",
        ProjectCreateView.as_view(),
        name="project-create",
    ),
    path("projects/", UserProjectsAPIView.as_view(), name="user-projects"),
]
