from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import compliance
from app.db import Base, engine

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Compliance Engine API",
    version="0.1.0",
    description="Enterprise KYB/KYC/AML compliance orchestration engine",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compliance.router, prefix="/api/v1")


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok", "service": "compliance-api", "version": "0.1.0"}
