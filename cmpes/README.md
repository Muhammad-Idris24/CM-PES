# Web-Based Contract Management and Performance Evaluation System

CMPES is a production-oriented Django information system for managing contract lifecycle, assigning contractors and supervisors, defining KPIs, evaluating performance, reviewing/approving evaluations, versioning contract documents, generating reports, auditing activity, and monitoring alerts from role-based dashboards.

## Local Setup

```powershell
cd C:\Users\user\Desktop\CM-PES\cmpes
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the public landing page or `/dashboard/` after login.

## Architecture

The application follows a three-tier web architecture:

Presentation Layer: Django templates, HTML5, CSS3, progressive JavaScript.
Application Layer: Django MTV apps for users, contracts, assignments, KPIs, evaluations, reports, and notifications.
Data Layer: SQLite for development and PostgreSQL in production through `DATABASE_URL`.

## Testing

```powershell
python manage.py test
python manage.py check --deploy
```

## Scheduled Alerts

Run this command daily from Render Cron Jobs or a host scheduler:

```powershell
python manage.py send_contract_alerts
```

Use `python manage.py send_contract_alerts --email` when production email settings are configured.

## Demo Data

For academic demonstrations:

```powershell
python manage.py seed_demo_data
```

Demo users use the password `DemoPass123!`.

## Documentation

See `docs/` for requirements, architecture diagrams, database schema, deployment notes, user manual, and endpoint inventory.
