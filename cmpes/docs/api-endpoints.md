# Endpoint List

This release uses secure server-rendered endpoints rather than a decoupled REST API.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Public landing page |
| GET | `/dashboard/` | Role dashboard |
| GET/POST | `/login/` | Session login |
| POST | `/logout/` | Session logout |
| GET | `/users/` | User list |
| GET/POST | `/users/new/` | Create user |
| GET/POST | `/users/<id>/edit/` | Edit user |
| GET | `/users/<id>/deactivate/` | Deactivate user |
| GET/POST | `/contracts/` | List contracts |
| GET/POST | `/contracts/new/` | Create contract |
| GET | `/contracts/<id>/` | Contract detail |
| GET/POST | `/contracts/<id>/edit/` | Edit contract |
| GET/POST | `/contracts/<id>/documents/new/` | Upload contract document version |
| GET | `/assignments/` | Assignment list |
| GET/POST | `/assignments/new/` | Create assignment |
| GET/POST | `/kpis/new/` | Create KPI |
| GET | `/evaluations/` | Evaluation list |
| GET/POST | `/evaluations/new/` | Create evaluation |
| GET | `/evaluations/<id>/` | Evaluation detail |
| POST | `/evaluations/<id>/REVIEWED/` | Mark evaluation reviewed |
| POST | `/evaluations/<id>/APPROVED/` | Approve evaluation |
| GET | `/reports/` | Report list |
| GET/POST | `/reports/new/` | Generate report |
| GET | `/notifications/` | Notification inbox |
