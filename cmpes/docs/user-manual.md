# User Manual

## Administrator

Log in, open Users, create staff and contractor accounts, assign roles, and deactivate accounts when needed. Use Contracts, Assignments, KPIs, Evaluations, Reports, and the audit activity feed to supervise all records.

## Manager/Evaluator

Create contracts, upload versioned documents, assign supervisors and contractors, define KPIs with weights, then create evaluations. Mark evaluations as reviewed or approved from the evaluation detail page. Reports can be printed from the report detail page.

## Contractor

Use the dashboard to view assigned contracts, responsibilities, KPIs, reports, notifications, and evaluation outcomes.

## Report Export

Open a report and use the Print button. Browser print can save the report as PDF.

## Notifications

Run `python manage.py send_contract_alerts` daily to create deadline and evaluation reminders.

Run `python manage.py send_contract_alerts --email` to also email recipients when email settings are configured.

## Demo Mode

Run `python manage.py seed_demo_data` to create realistic demo users, a contract, assignments, KPIs, an approved evaluation, and a report for academic presentation.
