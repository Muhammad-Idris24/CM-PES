from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from assignments.models import ContractAssignment
from contracts.models import Contract
from notifications.models import Notification
from users.models import User


class NotificationCommandTests(TestCase):
    def test_deadline_command_creates_alerts(self):
        manager = User.objects.create_user("manager@example.com", "Passw0rd!", full_name="Manager", role=User.Role.MANAGER)
        contractor = User.objects.create_user("contractor@example.com", "Passw0rd!", full_name="Contractor", role=User.Role.CONTRACTOR)
        contract = Contract.objects.create(
            title="Cleaning",
            description="Facility cleaning",
            start_date=timezone.localdate(),
            end_date=timezone.localdate() + timedelta(days=3),
            status=Contract.Status.ACTIVE,
            created_by=manager,
        )
        ContractAssignment.objects.create(contract=contract, user=contractor, role_in_contract=ContractAssignment.RoleInContract.CONTRACTOR)
        call_command("send_contract_alerts")
        self.assertEqual(Notification.objects.count(), 2)
