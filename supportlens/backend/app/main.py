from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_all_tables
from app.services.seed import seed_database
from app.routers import traces, analytics


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    await create_all_tables()
    await seed_database()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="SupportLens API",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(traces.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
