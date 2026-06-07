from django.conf import settings
from django.db import models


class ContractAssignment(models.Model):
    class RoleInContract(models.TextChoices):
        CONTRACTOR = "CONTRACTOR", "Contractor"
        SUPERVISOR = "SUPERVISOR", "Supervisor"

    contract = models.ForeignKey("contracts.Contract", on_delete=models.CASCADE, related_name="assignments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contract_assignments")
    role_in_contract = models.CharField(max_length=20, choices=RoleInContract.choices)
    responsibility = models.CharField(max_length=255, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("contract", "user", "role_in_contract")
        ordering = ["contract__title", "role_in_contract", "user__full_name"]

    def __str__(self):
        return f"{self.user.full_name} - {self.contract.title} ({self.get_role_in_contract_display()})"
