from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, Base
from routers import auth, devices, users, audit_logs

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "ngrok-skip-browser-warning"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(devices.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(audit_logs.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Auto-Vision FastAPI backend is running!"}
