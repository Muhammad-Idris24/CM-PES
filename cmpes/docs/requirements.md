# Requirement Synthesis

## Users

Administrator: manages users, contracts, assignments, KPIs, evaluations, reports, and monitoring.
Manager/Evaluator: manages contracts, assignments, KPIs, evaluations, reports, and operational monitoring.
Contractor: views assigned contracts, KPI definitions, evaluation results, reports, and notifications.

## Functional Modules

User Management: create users, assign roles, deactivate accounts.
Contract Management: create/edit contracts, upload documents, track deadlines, update lifecycle status.
Assignment System: assign contractors and supervisors with responsibilities.
KPI Management: define contract-specific KPI names, descriptions, and decimal weights.
Evaluation System: record KPI scores and compute `Total Score = sum(KPI Score x KPI Weight)`.
Reporting System: generate performance, summary, and analytics reports in print/export-ready HTML.
Notifications: create deadline and evaluation reminder alerts through a scheduled management command.

## Internal Validation

The implementation maps each chapter-derived data entity to a normalized Django model with foreign keys and referential integrity. Role access is enforced in views, templates, admin, and tests. Server-rendered pages keep the system aligned with the mandated Django/HTML/CSS/JavaScript stack.
