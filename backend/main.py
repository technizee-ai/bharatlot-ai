
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Bharatlot AI API",
    description="AI-powered e-commerce intelligence platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Bharatlot AI Backend is running!",
        "status": "healthy"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Bharatlot AI",
        "version": "1.0.0"
    }
