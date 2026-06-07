from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Evaluation(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        REVIEWED = "REVIEWED", "Reviewed"
        APPROVED = "APPROVED", "Approved"

    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="evaluations_made")
    contract = models.ForeignKey("contracts.Contract", on_delete=models.CASCADE, related_name="evaluations")
    total_score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="evaluations_reviewed", null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="evaluations_approved", null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.contract.title} evaluation ({self.total_score})"

    def recompute_total(self):
        total = Decimal("0")
        for detail in self.details.select_related("kpi"):
            total += Decimal(detail.score) * detail.kpi.weight
        self.total_score = total.quantize(Decimal("0.01"))
        self.save(update_fields=["total_score"])
        return self.total_score


class EvaluationDetail(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="details")
    kpi = models.ForeignKey("kpis.KPI", on_delete=models.PROTECT, related_name="evaluation_details")
    score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        unique_together = ("evaluation", "kpi")
        ordering = ["kpi__name"]

    def __str__(self):
        return f"{self.kpi.name}: {self.score}"
