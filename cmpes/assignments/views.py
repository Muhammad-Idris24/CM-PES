from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from users.models import User

from .forms import ContractAssignmentForm
from .models import ContractAssignment


class AssignmentListView(LoginRequiredMixin, ListView):
    model = ContractAssignment
    template_name = "assignments/assignment_list.html"
    context_object_name = "assignments"

    def get_queryset(self):
        qs = ContractAssignment.objects.select_related("contract", "user")
        if self.request.user.role == User.Role.CONTRACTOR:
            qs = qs.filter(user=self.request.user)
        return qs


class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = ContractAssignment
    form_class = ContractAssignmentForm
    template_name = "form.html"
    success_url = reverse_lazy("assignment_list")
    extra_context = {"title": "Assign Contract Responsibility"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in (User.Role.ADMIN, User.Role.MANAGER):
            messages.error(request, "Only administrators and managers can manage assignments.")
            return redirect("assignment_list")
        return super().dispatch(request, *args, **kwargs)


class AssignmentUpdateView(AssignmentCreateView, UpdateView):
    extra_context = {"title": "Edit Assignment"}
