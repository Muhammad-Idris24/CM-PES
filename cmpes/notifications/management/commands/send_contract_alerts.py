from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from audit.models import AuditLog
from audit.services import write_audit
from contracts.models import Contract
from notifications.models import Notification
from users.models import User


class Command(BaseCommand):
    help = "Create deadline and evaluation reminder notifications."

    def add_arguments(self, parser):
        parser.add_argument("--email", action="store_true", help="Also send notification emails.")

    def _notify(self, recipient, contract, notification_type, message, send_email):
        notification, was_created = Notification.objects.get_or_create(
            recipient=recipient,
            contract=contract,
            notification_type=notification_type,
            message=message,
        )
        if send_email and recipient.email and not notification.email_sent:
            send_mail(
                subject="CMPES Notification",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=True,
            )
            notification.email_sent = True
            notification.email_sent_at = timezone.now()
            notification.save(update_fields=["email_sent", "email_sent_at"])
        if was_created:
            write_audit(None, AuditLog.Action.NOTIFIED, notification, f"Notification created for {recipient.email}")
        return was_created

    def handle(self, *args, **options):
        send_email = options["email"]
        today = timezone.localdate()
        deadline = today + timedelta(days=7)
        contracts = Contract.objects.filter(status=Contract.Status.ACTIVE, end_date__lte=deadline, end_date__gte=today)
        recipients = User.objects.filter(is_active=True).exclude(role=User.Role.CONTRACTOR)
        created = 0
        for contract in contracts:
            for user in recipients:
                was_created = self._notify(
                    user,
                    contract,
                    Notification.NotificationType.DEADLINE,
                    f"{contract.title} ends on {contract.end_date}.",
                    send_email,
                )
                created += int(was_created)
            for assignment in contract.assignments.select_related("user"):
                was_created = self._notify(
                    assignment.user,
                    contract,
                    Notification.NotificationType.EVALUATION,
                    f"Performance review reminder for {contract.title}.",
                    send_email,
                )
                created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Created {created} notification(s)."))
