# Enterprise KYB / KYC / AML Compliance Engine

This repository packages the architecture described in the ADR into a working MVP for a white-label compliance orchestration platform tailored for Kenya and East Africa.

## What is included

- White-label onboarding form for vendors and suppliers
- Executive review dashboard for compliance officers
- FastAPI backend with compliance case endpoints
- React frontend for operator actions
- Docker Compose environment with Postgres and worker containers
- Guidance for local AML watchlist integration

## Architecture

- Web UI: React + Vite
- API: FastAPI
- Orchestration: Ballerine-inspired operations model
- AML engine: local watchlist matching layer ready to connect
- KYB worker: Playwright-style automation service
- KYC worker: OCR and ID validation worker
- Deployment: Docker Compose

## Repository layout

- `apps/web` – white-label client portal and dashboard
- `apps/api` – FastAPI backend and compliance routes
- `services/kyb_worker` – automated KYB verification worker
- `services/kyc_worker` – OCR and identity matching worker
- `services/aml_engine` – sanctions and PEP screening service
- `docker-compose.yml` – local orchestration setup
- `Makefile` – quick run commands

## Quick start

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:5173
- API docs: http://localhost:8001/docs
- PostgreSQL: localhost:5432

## Sample enterprise flows

- Vendor onboarding and ODPC consent capture
- Compliance review dashboard
- Risk and score snapshot by check type
- Audit-ready compliance case lifecycle

## Notes

This is a functioning MVP starter designed to be extended for government integrations, OCR pipelines, sanctions ingestion, PDF exports, and production deployment.
