from django.urls import path

from . import views

urlpatterns = [
    path("", views.KPIListView.as_view(), name="kpi_list"),
    path("new/", views.KPICreateView.as_view(), name="kpi_create"),
    path("<int:pk>/edit/", views.KPIUpdateView.as_view(), name="kpi_update"),
]
