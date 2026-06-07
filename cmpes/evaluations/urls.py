from django.urls import path

from . import views

urlpatterns = [
    path("", views.EvaluationListView.as_view(), name="evaluation_list"),
    path("new/", views.create_evaluation, name="evaluation_create"),
    path("<int:pk>/", views.EvaluationDetailView.as_view(), name="evaluation_detail"),
    path("<int:pk>/<str:status>/", views.update_evaluation_status, name="evaluation_status_update"),
]
