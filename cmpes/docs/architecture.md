# System Design

## Three-Tier Architecture

```mermaid
flowchart LR
  U["Users: Admin, Manager, Contractor"] --> P["Presentation Layer: Templates, HTML5, CSS3, JavaScript"]
  P --> A["Application Layer: Django MTV Apps"]
  A --> D["Data Layer: SQLite Development / PostgreSQL Production"]
  A --> N["Notification Command"]
  A --> R["Reporting Engine"]
```

## Data Flow

```mermaid
sequenceDiagram
  participant Manager
  participant Django
  participant DB
  Manager->>Django: Create contract and KPIs
  Django->>DB: Persist contract, assignments, KPIs
  Manager->>Django: Submit KPI scores
  Django->>DB: Save evaluation details
  Django->>Django: Compute weighted total
  Django->>DB: Store evaluation history
  Manager->>Django: Generate report
  Django->>DB: Read contract/evaluation data
  Django-->>Manager: Print-ready report
```

## Navigation Structure

Dashboard, Contracts, Assignments, KPIs, Evaluations, Reports, Notifications, Users.

## URL Routing Plan

`/` dashboard
`/login/`, `/logout/` authentication
`/users/` administration
`/contracts/` lifecycle management
`/assignments/` contractor and supervisor assignment
`/kpis/` KPI definition
`/evaluations/` performance evaluation
`/reports/` reporting
`/notifications/` alerts
