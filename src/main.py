from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from src.apis.egramswaraj import EGramSwarajUnavailable
from src.routes.panchayats import router as panchayat_router


load_dotenv("dev.env")


app = FastAPI(
    title="Udupi GoUdupi Backend",
    description="Backend API for Udupi GoUdupi frontend",
    version="0.1.0",
)


@app.exception_handler(EGramSwarajUnavailable)
async def egramswaraj_unavailable_handler(
    request: Request,
    exc: EGramSwarajUnavailable,
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Government planning data is temporarily unavailable. Please retry shortly."
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://go-udupi.vercel.app",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(panchayat_router)
