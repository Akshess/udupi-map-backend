from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from src.routes.panchayats import router as panchayat_router

load_dotenv("dev.env")


app = FastAPI(
    title="Udupi GoUdupi Backend",
    description="Backend API for Udupi GoUdupi frontend",
    version="0.1.0",
)

# Allow your frontend (localhost + deployed URL) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://go-udupi.vercel.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(panchayat_router)

