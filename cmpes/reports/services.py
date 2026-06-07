from django.db.models import Avg

from evaluations.models import Evaluation


def build_report_content(contract, report_type):
    evaluations = Evaluation.objects.filter(contract=contract).prefetch_related("details__kpi")
    average_score = evaluations.aggregate(value=Avg("total_score"))["value"]
    lines = [
        f"Contract: {contract.title}",
        f"Status: {contract.get_status_display()}",
        f"Period: {contract.start_date} to {contract.end_date}",
        f"Evaluations completed: {evaluations.count()}",
        f"Average score: {average_score or 0}",
        f"Approved evaluations: {evaluations.filter(status='APPROVED').count()}",
        "",
        "Recent evaluation notes:",
    ]
    for evaluation in evaluations[:5]:
        lines.append(f"- {evaluation.created_at:%Y-%m-%d}: {evaluation.total_score} ({evaluation.get_status_display()}) - {evaluation.feedback or 'No feedback'}")
    if report_type == "CONTRACT_SUMMARY":
        lines.extend(["", "Description:", contract.description])
    if report_type == "EVALUATION_ANALYTICS":
        lines.append("")
        lines.append("KPI score breakdown:")
        for evaluation in evaluations:
            for detail in evaluation.details.all():
                lines.append(f"- {detail.kpi.name}: {detail.score} x {detail.kpi.weight}")
    return "\n".join(lines)
