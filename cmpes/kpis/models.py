from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class KPI(models.Model):
    contract = models.ForeignKey("contracts.Contract", on_delete=models.CASCADE, related_name="kpis")
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "KPI"
        verbose_name_plural = "KPIs"
        unique_together = ("contract", "name")
        ordering = ["contract__title", "name"]

    def __str__(self):
        return f"{self.name} ({self.contract.title})"
