from django.urls import path

from . import views

urlpatterns = [
    path("", views.ReportListView.as_view(), name="report_list"),
    path("new/", views.ReportCreateView.as_view(), name="report_create"),
    path("<int:pk>/", views.ReportDetailView.as_view(), name="report_detail"),
]
