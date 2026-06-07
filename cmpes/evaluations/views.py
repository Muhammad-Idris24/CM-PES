from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView

from audit.models import AuditLog
from audit.services import write_audit
from contracts.models import Contract
from kpis.models import KPI
from users.models import User

from .forms import EvaluationForm
from .models import Evaluation, EvaluationDetail


class EvaluationListView(LoginRequiredMixin, ListView):
    model = Evaluation
    template_name = "evaluations/evaluation_list.html"
    context_object_name = "evaluations"

    def get_queryset(self):
        qs = Evaluation.objects.select_related("contract", "evaluator")
        if self.request.user.role == User.Role.CONTRACTOR:
            qs = qs.filter(contract__assignments__user=self.request.user).distinct()
        return qs


class EvaluationDetailView(LoginRequiredMixin, DetailView):
    model = Evaluation
    template_name = "evaluations/evaluation_detail.html"
    context_object_name = "evaluation"

    def get_queryset(self):
        qs = Evaluation.objects.select_related("contract", "evaluator").prefetch_related("details__kpi")
        if self.request.user.role == User.Role.CONTRACTOR:
            qs = qs.filter(contract__assignments__user=self.request.user).distinct()
        return qs


def create_evaluation(request):
    if request.user.role not in (User.Role.ADMIN, User.Role.MANAGER):
        messages.error(request, "Only administrators and managers can evaluate contracts.")
        return redirect("evaluation_list")
    form = EvaluationForm(request.POST or None)
    contract = None
    kpis = KPI.objects.none()
    if request.method == "POST" and request.POST.get("contract"):
        contract = get_object_or_404(Contract, pk=request.POST["contract"])
        kpis = contract.kpis.all()
    elif request.GET.get("contract"):
        contract = get_object_or_404(Contract, pk=request.GET["contract"])
        form = EvaluationForm(initial={"contract": contract})
        kpis = contract.kpis.all()
    if request.method == "POST" and form.is_valid():
        contract = form.cleaned_data["contract"]
        kpis = list(contract.kpis.all())
        if not kpis:
            messages.error(request, "Define KPIs before evaluating this contract.")
            return redirect("kpi_create")
        with transaction.atomic():
            evaluation = form.save(commit=False)
            evaluation.evaluator = request.user
            evaluation.save()
            for kpi in kpis:
                score = request.POST.get(f"score_{kpi.pk}")
                if score not in (None, ""):
                    EvaluationDetail.objects.create(evaluation=evaluation, kpi=kpi, score=score)
            evaluation.recompute_total()
            write_audit(
                request.user,
                AuditLog.Action.EVALUATED,
                evaluation,
                f"Evaluation recorded for {contract.title} with score {evaluation.total_score}",
                request=request,
            )
        messages.success(request, "Evaluation saved and total score calculated.")
        return redirect("evaluation_detail", pk=evaluation.pk)
    return render(request, "evaluations/evaluation_form.html", {"form": form, "kpis": kpis, "contract": contract, "title": "New Evaluation"})


def update_evaluation_status(request, pk, status):
    if request.method != "POST":
        messages.error(request, "Use the evaluation action buttons to update status.")
        return redirect("evaluation_detail", pk=pk)
    if request.user.role not in (User.Role.ADMIN, User.Role.MANAGER):
        messages.error(request, "Only administrators and managers can update evaluation status.")
        return redirect("evaluation_detail", pk=pk)
    evaluation = get_object_or_404(Evaluation, pk=pk)
    now = timezone.now()
    if status == Evaluation.Status.REVIEWED:
        evaluation.status = status
        evaluation.reviewed_by = request.user
        evaluation.reviewed_at = now
        action = AuditLog.Action.REVIEWED
        message = "Evaluation marked as reviewed."
    elif status == Evaluation.Status.APPROVED:
        evaluation.status = status
        evaluation.approved_by = request.user
        evaluation.approved_at = now
        action = AuditLog.Action.APPROVED
        message = "Evaluation approved."
    else:
        messages.error(request, "Unsupported evaluation status.")
        return redirect("evaluation_detail", pk=pk)
    evaluation.save()
    write_audit(request.user, action, evaluation, f"{evaluation.contract.title} evaluation {evaluation.get_status_display().lower()}", request=request)
    messages.success(request, message)
    return redirect(reverse("evaluation_detail", args=[evaluation.pk]))
