#!/usr/bin/env python3
"""Prosty test FastAPI"""

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Test API")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    return {"status": "OK", "message": "Test endpoint działa"}

if __name__ == "__main__":
    print("🚀 Uruchamianie testowego FastAPI...")
    uvicorn.run(
        "test_fastapi:app",
        host="0.0.0.0",
        port=8001,
        reload=False
    )