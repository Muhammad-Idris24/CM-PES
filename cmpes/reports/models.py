from django.conf import settings
from django.db import models


class Report(models.Model):
    class ReportType(models.TextChoices):
        PERFORMANCE = "PERFORMANCE", "Performance Report"
        CONTRACT_SUMMARY = "CONTRACT_SUMMARY", "Contract Summary"
        EVALUATION_ANALYTICS = "EVALUATION_ANALYTICS", "Evaluation Analytics"

    contract = models.ForeignKey("contracts.Contract", on_delete=models.CASCADE, related_name="reports")
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reports_generated")
    report_type = models.CharField(max_length=30, choices=ReportType.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.contract.title}"
