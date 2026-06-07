from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from contracts.models import Contract, ContractDocument
from users.models import User


class ContractDocumentTests(TestCase):
    def test_manager_can_upload_document_version(self):
        manager = User.objects.create_user("manager@example.com", "Passw0rd!", full_name="Manager", role=User.Role.MANAGER)
        contract = Contract.objects.create(
            title="Supply Agreement",
            description="Supply contract",
            start_date="2026-01-01",
            end_date="2026-12-31",
            status=Contract.Status.ACTIVE,
            created_by=manager,
        )
        self.client.force_login(manager)
        response = self.client.post(reverse("contract_document_create", args=[contract.pk]), {
            "title": "Signed Contract",
            "document_type": ContractDocument.DocumentType.CONTRACT,
            "version": 1,
            "notes": "Initial signed copy",
            "file": SimpleUploadedFile("contract.txt", b"contract terms"),
        })
        self.assertRedirects(response, contract.get_absolute_url())
        self.assertEqual(contract.documents.count(), 1)

# Create your tests here.
