from django.urls import path

from . import views

urlpatterns = [
    path("", views.AssignmentListView.as_view(), name="assignment_list"),
    path("new/", views.AssignmentCreateView.as_view(), name="assignment_create"),
    path("<int:pk>/edit/", views.AssignmentUpdateView.as_view(), name="assignment_update"),
]
