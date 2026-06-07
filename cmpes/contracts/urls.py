from django.urls import path

from . import views

urlpatterns = [
    path("", views.ContractListView.as_view(), name="contract_list"),
    path("new/", views.ContractCreateView.as_view(), name="contract_create"),
    path("<int:pk>/", views.ContractDetailView.as_view(), name="contract_detail"),
    path("<int:pk>/edit/", views.ContractUpdateView.as_view(), name="contract_update"),
    path("<int:pk>/documents/new/", views.ContractDocumentCreateView.as_view(), name="contract_document_create"),
]
