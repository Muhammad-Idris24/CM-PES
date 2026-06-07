from django.conf import settings
from django.db import models
from django.urls import reverse


class Contract(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        TERMINATED = "TERMINATED", "Terminated"

    title = models.CharField(max_length=180)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="contracts_created")
    document = models.FileField(upload_to="contract_documents/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "end_date"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("contract_detail", args=[self.pk])


class ContractDocument(models.Model):
    class DocumentType(models.TextChoices):
        CONTRACT = "CONTRACT", "Contract Document"
        ADDENDUM = "ADDENDUM", "Addendum"
        EVIDENCE = "EVIDENCE", "Performance Evidence"
        OTHER = "OTHER", "Other"

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=180)
    document_type = models.CharField(max_length=20, choices=DocumentType.choices, default=DocumentType.CONTRACT)
    file = models.FileField(upload_to="contract_documents/versions/")
    version = models.PositiveIntegerField(default=1)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="contract_documents_uploaded")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-uploaded_at"]
        unique_together = ("contract", "version", "title")

    def __str__(self):
        return f"{self.contract.title} - {self.title} v{self.version}"
