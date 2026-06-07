from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from audit.models import AuditLog
from audit.services import write_audit
from users.models import User

from .models import Report
from .services import build_report_content


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = "reports/report_list.html"
    context_object_name = "reports"

    def get_queryset(self):
        qs = Report.objects.select_related("contract", "generated_by")
        if self.request.user.role == User.Role.CONTRACTOR:
            qs = qs.filter(contract__assignments__user=self.request.user).distinct()
        return qs


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = "reports/report_detail.html"
    context_object_name = "report"


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    fields = ("contract", "report_type")
    template_name = "form.html"
    success_url = reverse_lazy("report_list")
    extra_context = {"title": "Generate Report"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in (User.Role.ADMIN, User.Role.MANAGER):
            messages.error(request, "Only administrators and managers can generate reports.")
            return redirect("report_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.generated_by = self.request.user
        form.instance.content = build_report_content(form.instance.contract, form.instance.report_type)
        messages.success(self.request, "Report generated.")
        response = super().form_valid(form)
        write_audit(
            self.request.user,
            AuditLog.Action.GENERATED,
            self.object,
            f"Generated {self.object.get_report_type_display()} for {self.object.contract.title}",
            request=self.request,
        )
        return response
