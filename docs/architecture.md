# NexHuman Architecture

## Planned architecture

```text
React frontend
      |
      v
Django REST API
      |
      +-- Authentication
      +-- Portfolio management
      +-- Market-data services
      +-- Evolutionary optimizer
      +-- AI advisor
      |
      v
PostgreSQL

## Backend Domains

The NexHuman backend is organised into domain-focused Django applications.

### Accounts
Responsible for user identity, email-based authentication, registration,
password management and administrative user management.

### Profiling
Responsible for investment-preference questionnaires, user responses,
calculated preference scores and user-friendly risk classifications.

### Portfolios
Responsible for user-owned portfolios and cryptocurrency holdings.

### Market Data
Responsible for supported cryptocurrency assets, historical market data,
external market-data provider integration and future market-intelligence
functionality.

### Optimizer
Responsible for the genetic algorithm, optimisation configuration,
execution, results and historical optimisation runs.

### Advisor
Responsible for persistent AI-advisor conversations and contextual
portfolio explanations.

## Backend Design Principles

- PostgreSQL is the primary database from the beginning of development.
- Authentication uses email and password rather than usernames.
- Django REST Framework provides the backend API.
- JWT access and refresh tokens are used for API authentication.
- API endpoints are versioned under `/api/v1/`.
- Business logic is separated from API views.
- Optimisation algorithms are separated from the Django web layer.
- Market data is accessed through the backend rather than directly by the frontend.
- Historical data required for optimisation is persisted for reproducibility.
- Optimisation runs and their results are retained for evaluation and auditability.
- Environment-specific configuration and secrets are not committed to source control.