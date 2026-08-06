from fastapi import APIRouter
from src.services.panchayat_service import get_panchayat_planning

router = APIRouter(
    prefix="/panchayats",
    tags=["Panchayats"],
)

@router.get("/{lgd_code}/planning")
async def planning(
    lgd_code: int,
    year: int,
):
    return await get_panchayat_planning(
        lgd_code=lgd_code,
        plan_year=year,
    )