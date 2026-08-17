from fastapi import FastAPI

_APP_VERSION = "0.0.0"

app = FastAPI()

@app.get("/")
def my_home():
    return {"message": "Welcome to TinyPulse"}

@app.get("/health")
def health():
    return {"version": _APP_VERSION, "status": "Backend is working fine !"}
