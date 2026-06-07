from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from assignments.models import ContractAssignment
from contracts.models import Contract
from evaluations.models import Evaluation, EvaluationDetail
from kpis.models import KPI
from reports.models import Report
from reports.services import build_report_content
from users.models import User


class Command(BaseCommand):
    help = "Seed CMPES with realistic demo users, contracts, KPIs, evaluations, and reports."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            email="demo.admin@cmpes.local",
            defaults={"full_name": "Demo Administrator", "role": User.Role.ADMIN, "is_staff": True, "is_superuser": True},
        )
        admin.set_password("DemoPass123!")
        admin.save()
        manager, _ = User.objects.get_or_create(
            email="demo.manager@cmpes.local",
            defaults={"full_name": "Ada Manager", "role": User.Role.MANAGER, "phone_number": "+234800000001"},
        )
        manager.set_password("DemoPass123!")
        manager.save()
        contractor, _ = User.objects.get_or_create(
            email="demo.contractor@cmpes.local",
            defaults={"full_name": "Northstar Contractors", "role": User.Role.CONTRACTOR, "phone_number": "+234800000002"},
        )
        contractor.set_password("DemoPass123!")
        contractor.save()

        today = timezone.localdate()
        contract, _ = Contract.objects.get_or_create(
            title="Facilities Maintenance 2026",
            defaults={
                "description": "Annual facilities maintenance contract covering preventive repairs, response time, and service quality.",
                "start_date": today - timedelta(days=45),
                "end_date": today + timedelta(days=120),
                "status": Contract.Status.ACTIVE,
                "created_by": manager,
            },
        )
        ContractAssignment.objects.get_or_create(
            contract=contract,
            user=contractor,
            role_in_contract=ContractAssignment.RoleInContract.CONTRACTOR,
            defaults={"responsibility": "Execute maintenance tasks and submit service evidence."},
        )
        ContractAssignment.objects.get_or_create(
            contract=contract,
            user=manager,
            role_in_contract=ContractAssignment.RoleInContract.SUPERVISOR,
            defaults={"responsibility": "Supervise delivery and perform monthly evaluations."},
        )
        kpi_data = [
            ("Quality of Work", Decimal("0.40"), "Workmanship and defect rate."),
            ("Timeliness", Decimal("0.30"), "Completion against agreed deadlines."),
            ("Compliance", Decimal("0.30"), "Safety, documentation, and policy compliance."),
        ]
        kpis = []
        for name, weight, description in kpi_data:
            kpi, _ = KPI.objects.get_or_create(contract=contract, name=name, defaults={"weight": weight, "description": description})
            kpis.append(kpi)
        evaluation, created = Evaluation.objects.get_or_create(
            contract=contract,
            evaluator=manager,
            feedback="Performance is strong with minor improvement needed in documentation turnaround.",
            defaults={"status": Evaluation.Status.APPROVED, "approved_by": admin, "approved_at": timezone.now()},
        )
        if created:
            for kpi, score in zip(kpis, [88, 84, 91]):
                EvaluationDetail.objects.create(evaluation=evaluation, kpi=kpi, score=score)
            evaluation.recompute_total()
        Report.objects.get_or_create(
            contract=contract,
            generated_by=manager,
            report_type=Report.ReportType.PERFORMANCE,
            defaults={"content": build_report_content(contract, Report.ReportType.PERFORMANCE)},
        )
        self.stdout.write(self.style.SUCCESS("Demo data ready. Password for demo users: DemoPass123!"))
