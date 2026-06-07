from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from users.models import User

from .forms import KPIForm
from .models import KPI


class KPIListView(LoginRequiredMixin, ListView):
    model = KPI
    template_name = "kpis/kpi_list.html"
    context_object_name = "kpis"

    def get_queryset(self):
        qs = KPI.objects.select_related("contract")
        if self.request.user.role == User.Role.CONTRACTOR:
            qs = qs.filter(contract__assignments__user=self.request.user).distinct()
        return qs


class KPICreateView(LoginRequiredMixin, CreateView):
    model = KPI
    form_class = KPIForm
    template_name = "form.html"
    success_url = reverse_lazy("kpi_list")
    extra_context = {"title": "Create KPI"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in (User.Role.ADMIN, User.Role.MANAGER):
            messages.error(request, "Only administrators and managers can manage KPIs.")
            return redirect("kpi_list")
        return super().dispatch(request, *args, **kwargs)


class KPIUpdateView(KPICreateView, UpdateView):
    extra_context = {"title": "Edit KPI"}
