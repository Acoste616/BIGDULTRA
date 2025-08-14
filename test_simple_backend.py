#!/usr/bin/env python3
"""Prosty test backendu Ultra BIGDecoder 3.0"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Inicjalizacja FastAPI
app = FastAPI(
    title="Ultra BIGDecoder 3.0 API - TEST",
    description="Test backendu bez lifespan",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint główny - test"""
    return {
        "name": "Ultra BIGDecoder 3.0 - TEST",
        "version": "3.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/test")
async def test():
    """Test endpoint"""
    return {"message": "Test OK", "status": "working"}

@app.post("/analyze")
async def test_analyze():
    """Test endpoint analizy"""
    return {
        "status": "test",
        "message": "Endpoint analizy działa",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("🚀 Uruchamianie testowego backendu...")
    uvicorn.run(
        "test_simple_backend:app",
        host="0.0.0.0",
        port=8002,
        reload=False,
        log_level="info"
    )