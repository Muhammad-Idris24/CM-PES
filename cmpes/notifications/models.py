from django.conf import settings
from django.db import models


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        DEADLINE = "DEADLINE", "Contract Deadline"
        EVALUATION = "EVALUATION", "Evaluation Reminder"
        STATUS = "STATUS", "Status Update"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    contract = models.ForeignKey("contracts.Contract", on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.message
