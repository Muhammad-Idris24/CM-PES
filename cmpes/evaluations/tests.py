from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from contracts.models import Contract
from evaluations.models import Evaluation, EvaluationDetail
from kpis.models import KPI
from users.models import User


class EvaluationWorkflowTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user("manager@example.com", "Passw0rd!", full_name="Manager", role=User.Role.MANAGER)
        self.contractor = User.objects.create_user("contractor@example.com", "Passw0rd!", full_name="Contractor", role=User.Role.CONTRACTOR)
        self.contract = Contract.objects.create(
            title="Road Works",
            description="Road rehabilitation",
            start_date="2026-01-01",
            end_date="2026-12-31",
            status=Contract.Status.ACTIVE,
            created_by=self.manager,
        )
        self.quality = KPI.objects.create(contract=self.contract, name="Quality", weight=Decimal("0.60"))
        self.timeliness = KPI.objects.create(contract=self.contract, name="Timeliness", weight=Decimal("0.40"))

    def test_total_score_is_weighted_sum(self):
        evaluation = Evaluation.objects.create(evaluator=self.manager, contract=self.contract, feedback="Good")
        EvaluationDetail.objects.create(evaluation=evaluation, kpi=self.quality, score=80)
        EvaluationDetail.objects.create(evaluation=evaluation, kpi=self.timeliness, score=90)
        self.assertEqual(evaluation.recompute_total(), Decimal("84.00"))

    def test_contractor_cannot_open_create_evaluation_page(self):
        self.client.force_login(self.contractor)
        response = self.client.get(reverse("evaluation_create"))
        self.assertRedirects(response, reverse("evaluation_list"))

    def test_manager_can_create_evaluation_from_kpi_scores(self):
        self.client.force_login(self.manager)
        response = self.client.post(reverse("evaluation_create"), {
            "contract": self.contract.pk,
            "feedback": "Meets expectations",
            f"score_{self.quality.pk}": "75",
            f"score_{self.timeliness.pk}": "85",
        })
        evaluation = Evaluation.objects.get()
        self.assertRedirects(response, reverse("evaluation_detail", args=[evaluation.pk]))
        self.assertEqual(evaluation.total_score, Decimal("79.00"))
        self.assertEqual(evaluation.status, Evaluation.Status.SUBMITTED)

    def test_manager_can_approve_evaluation(self):
        evaluation = Evaluation.objects.create(evaluator=self.manager, contract=self.contract, feedback="Ready")
        self.client.force_login(self.manager)
        response = self.client.post(reverse("evaluation_status_update", args=[evaluation.pk, Evaluation.Status.APPROVED]))
        evaluation.refresh_from_db()
        self.assertRedirects(response, reverse("evaluation_detail", args=[evaluation.pk]))
        self.assertEqual(evaluation.status, Evaluation.Status.APPROVED)
        self.assertEqual(evaluation.approved_by, self.manager)
