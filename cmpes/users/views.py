from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView

from audit.models import AuditLog
from audit.services import write_audit
from assignments.models import ContractAssignment
from contracts.models import Contract
from evaluations.models import Evaluation
from kpis.models import KPI
from reports.models import Report

from .decorators import role_required
from .forms import UserAdminForm, UserCreationForm
from .models import User


def landing(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "landing.html")


@login_required
def dashboard(request):
    user = request.user
    today = timezone.localdate()
    deadline_window = today + timezone.timedelta(days=14)
    base = {
        "contract_count": Contract.objects.count(),
        "active_contracts": Contract.objects.filter(status=Contract.Status.ACTIVE).count(),
        "evaluation_count": Evaluation.objects.count(),
        "average_score": Evaluation.objects.aggregate(value=Avg("total_score"))["value"] or 0,
        "upcoming_deadlines": Contract.objects.filter(status=Contract.Status.ACTIVE, end_date__range=(today, deadline_window)).count(),
        "approved_evaluations": Evaluation.objects.filter(status=Evaluation.Status.APPROVED).count(),
    }
    if user.role == User.Role.CONTRACTOR:
        assignments = ContractAssignment.objects.filter(user=user).select_related("contract")
        contracts = Contract.objects.filter(assignments__user=user).distinct()
        return render(request, "users/dashboard_contractor.html", {
            **base,
            "assignments": assignments,
            "contracts": contracts,
            "recent_evaluations": Evaluation.objects.filter(contract__in=contracts).select_related("contract")[:5],
        })
    if user.role == User.Role.MANAGER:
        return render(request, "users/dashboard_manager.html", {
            **base,
            "recent_evaluations": Evaluation.objects.select_related("contract")[:5],
            "contracts_by_status": Contract.objects.values("status").annotate(total=Count("id")),
            "pending_reviews": Evaluation.objects.exclude(status=Evaluation.Status.APPROVED).count(),
        })
    return render(request, "users/dashboard_admin.html", {
        **base,
        "user_count": User.objects.count(),
        "kpi_count": KPI.objects.count(),
        "report_count": Report.objects.count(),
        "contracts_by_status": Contract.objects.values("status").annotate(total=Count("id")),
        "recent_audit_logs": AuditLog.objects.select_related("actor")[:8],
    })


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.role == User.Role.ADMIN):
            messages.error(request, "Only administrators can manage users.")
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "form.html"
    success_url = reverse_lazy("user_list")
    extra_context = {"title": "Create User"}

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.role == User.Role.ADMIN):
            messages.error(request, "Only administrators can create users.")
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        write_audit(self.request.user, AuditLog.Action.CREATED, self.object, f"User created: {self.object.email}", request=self.request)
        return response


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserAdminForm
    template_name = "form.html"
    success_url = reverse_lazy("user_list")
    extra_context = {"title": "Edit User"}

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.role == User.Role.ADMIN):
            messages.error(request, "Only administrators can edit users.")
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        write_audit(self.request.user, AuditLog.Action.UPDATED, self.object, f"User updated: {self.object.email}", request=self.request)
        return response


@role_required(User.Role.ADMIN)
def deactivate_user(request, pk):
    user = User.objects.get(pk=pk)
    if user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
    else:
        user.is_active = False
        user.save(update_fields=["is_active"])
        write_audit(request.user, AuditLog.Action.DEACTIVATED, user, f"User deactivated: {user.email}", request=request)
        messages.success(request, "User account deactivated.")
    return redirect("user_list")
