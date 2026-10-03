# Enterprise KYB / KYC / AML Compliance Engine

A white-label, zero API cost compliance orchestration platform for Kenya and East Africa. This repository contains a working MVP of the architecture described in the ADR.

## What's included

✅ React white-label web app with onboarding and review dashboard
✅ FastAPI backend with compliance case persistence
✅ PostgreSQL database for case storage
✅ Docker Compose multi-service environment
✅ Worker services scaffolding (KYB, KYC, AML)
✅ CORS-enabled API for frontend integration
✅ Responsive UI with Tailwind-inspired styling

## Quick start

### Prerequisites

- Docker & Docker Compose installed
- Git

### Installation

```bash
git clone https://github.com/Woka21/enterprise-kyb-kyc-aml-engine.git
cd enterprise-kyb-kyc-aml-engine

# Start all services
docker compose up --build
```

Then open:

- **Frontend:** http://localhost:5173
- **API Docs:** http://localhost:8001/docs
- **PostgreSQL:** localhost:5432 (user: `compliance`, pass: `compliance_secret`)

### Make commands

```bash
make up          # Start all services with build
make down        # Stop all services
make logs        # Tail all service logs
make api-logs    # Tail API logs only
make web-logs    # Tail web logs only
making db-logs   # Tail PostgreSQL logs only
```

## Architecture

```
┌─────────────────────────────────┐
│  React Web App (Port 5173)      │
│  - Onboarding form              │
│  - Review dashboard             │
│  - Live case updates            │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│  FastAPI Backend (Port 8001)    │
│  - Case submission endpoint     │
│  - Case listing & status        │
│  - Database operations          │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│  PostgreSQL (Port 5432)         │
│  - Compliance cases table       │
│  - Case history & timestamps    │
└─────────────────────────────────┘
```

## API Endpoints

- **GET /api/v1/compliance/cases** – List all cases
- **POST /api/v1/compliance/submit** – Submit new case
- **GET /api/v1/compliance/status/{case_id}** – Get case details
- **GET /health** – Health check

## Sample workflow

1. Open http://localhost:5173
2. Fill in the vendor onboarding form
3. Submit for verification
4. Check the executive dashboard to see your case
5. Scores update in real-time as worker services process

## Features

- Vendor onboarding with ODPC consent
- KYB score tracking
- KYC identity matching score
- AML / PEP sanctions screening
- Case clearance status tracking
- Risk level classification
- Document type management
- Automatic timestamp tracking
- Live case database persistence

## Next steps

- Connect KYB worker to KRA PIN verification API
- Integrate Tesseract OCR for ID document parsing
- Add OpenSanctions database for AML matching
- Implement PDF compliance certificate export
- Add multi-tenant white-label domain support
- Deploy to production VPS with Nginx + SSL
- Add SMS/Email notifications
- Implement audit logging and compliance reports

## Environment variables

Create `.env` file in repository root:

```env
DATABASE_URL=postgresql://compliance:compliance_secret@postgres:5432/compliance
VITE_API_URL=http://localhost:8001
APP_ENV=development
```

## License

MIT

## Support

For questions or issues, open a GitHub issue in this repository.
