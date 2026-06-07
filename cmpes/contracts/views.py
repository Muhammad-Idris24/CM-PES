from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from audit.models import AuditLog
from audit.services import write_audit
from users.models import User

from .forms import ContractDocumentForm, ContractForm
from .models import Contract


class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = "contracts/contract_list.html"
    context_object_name = "contracts"

    def get_queryset(self):
        qs = Contract.objects.select_related("created_by").prefetch_related("assignments__user")
        if self.request.user.role == User.Role.CONTRACTOR:
            qs = qs.filter(assignments__user=self.request.user).distinct()
        return qs


class ContractDetailView(LoginRequiredMixin, DetailView):
    model = Contract
    template_name = "contracts/contract_detail.html"
    context_object_name = "contract"

    def get_queryset(self):
        qs = Contract.objects.select_related("created_by").prefetch_related("assignments__user", "kpis", "evaluations", "documents")
        if self.request.user.role == User.Role.CONTRACTOR:
            qs = qs.filter(assignments__user=self.request.user).distinct()
        return qs


class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = "form.html"
    success_url = reverse_lazy("contract_list")
    extra_context = {"title": "Create Contract"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in (User.Role.ADMIN, User.Role.MANAGER):
            messages.error(request, "Only administrators and managers can create contracts.")
            return redirect("contract_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        is_new = form.instance.pk is None
        form.instance.created_by = self.request.user
        messages.success(self.request, "Contract saved.")
        response = super().form_valid(form)
        write_audit(
            self.request.user,
            AuditLog.Action.CREATED if is_new else AuditLog.Action.UPDATED,
            self.object,
            f"Contract {'created' if is_new else 'updated'}: {self.object.title}",
            request=self.request,
        )
        return response


class ContractUpdateView(ContractCreateView, UpdateView):
    extra_context = {"title": "Edit Contract"}


class ContractDocumentCreateView(LoginRequiredMixin, CreateView):
    form_class = ContractDocumentForm
    template_name = "form.html"
    extra_context = {"title": "Upload Contract Document"}

    def dispatch(self, request, *args, **kwargs):
        self.contract = get_object_or_404(Contract, pk=kwargs["pk"])
        if request.user.role not in (User.Role.ADMIN, User.Role.MANAGER):
            messages.error(request, "Only administrators and managers can upload contract documents.")
            return redirect(self.contract)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.contract = self.contract
        form.instance.uploaded_by = self.request.user
        response = super().form_valid(form)
        write_audit(
            self.request.user,
            AuditLog.Action.CREATED,
            self.object,
            f"Uploaded document {self.object.title} for {self.contract.title}",
            request=self.request,
        )
        messages.success(self.request, "Document uploaded.")
        return response

    def get_success_url(self):
        return self.contract.get_absolute_url()
