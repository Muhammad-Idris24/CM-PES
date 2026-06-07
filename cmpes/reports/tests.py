from django.test import TestCase

from contracts.models import Contract
from reports.services import build_report_content
from users.models import User


class ReportServiceTests(TestCase):
    def test_contract_summary_contains_core_contract_data(self):
        user = User.objects.create_user("manager@example.com", "Passw0rd!", full_name="Manager", role=User.Role.MANAGER)
        contract = Contract.objects.create(
            title="ICT Support",
            description="Help desk coverage",
            start_date="2026-01-01",
            end_date="2026-06-30",
            status=Contract.Status.ACTIVE,
            created_by=user,
        )
        content = build_report_content(contract, "CONTRACT_SUMMARY")
        self.assertIn("ICT Support", content)
        self.assertIn("Help desk coverage", content)
