#!/usr/bin/env python3
"""
Simple test script for Railway deployment
"""

from fastapi import FastAPI

app = FastAPI(title="Subscription Tracker Test")

@app.get("/")
def root():
    return {"message": "Hello from Railway!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "Subscription Tracker"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
