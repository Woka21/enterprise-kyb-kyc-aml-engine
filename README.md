# Enterprise KYB / KYC / AML Compliance Engine

This repository packages the architecture described in the ADR into a working starter project for a white-label compliance orchestration platform tailored for Kenya and East Africa.

## Overview

The system is designed to support:

- Corporate verification (KYB)
- Director identity matching (KYC)
- AML / PEP screening
- Case workflow orchestration
- PDF-ready audit outputs
- White-label deployment for enterprise clients

## Architecture

- Web UI: React + Vite
- API: FastAPI
- Orchestration: Ballerine-inspired workflow service
- AML engine: local OpenSanctions-style matching with PostgreSQL
- KYB worker: Playwright-based public checker worker
- KYC worker: OCR + facial comparison worker
- Container orchestration: Docker Compose

## Repository layout

- `apps/web` – white-label client portal and operator dashboard
- `apps/api` – FastAPI backend and orchestration endpoints
- `services/kyb_worker` – automated KYB verification worker
- `services/kyc_worker` – OCR and ID document processing worker
- `services/aml_engine` – AML / sanctions matching service
- `docker-compose.yml` – local environment

## Quick start

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:5173
- API docs: http://localhost:8001/docs
- PostgreSQL: localhost:5432

## Sample enterprise flows

- Vendor onboarding form
- Compliance review dashboard
- PDF certificate generation
- National ID / passport verification
- Sanctions and PEP screening

## Notes

This is a starter implementation focused on architecture and workflow structure. It is intentionally designed to be extensible for real integration with government portals, OCR tooling, and sanctions data ingestion.
