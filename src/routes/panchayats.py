from fastapi import APIRouter

from src.services.panchayat_service import (
    get_panchayat_planning,
    get_panchayat_activities,
    get_panchayat_resource_envelope,
    get_panchayat_physical_progress,
)

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


@router.get("/{lgd_code}/activities")
async def activities(
    lgd_code: int,
    plan_year: int,
):
    return await get_panchayat_activities(
        lgd_code=lgd_code,
        plan_year=plan_year,
    )


@router.get("/{lgd_code}/resource-envelope")
async def resource_envelope(
    lgd_code: int,
    plan_year: int,
):
    return await get_panchayat_resource_envelope(
        lgd_code=lgd_code,
        plan_year=plan_year,
    )


@router.get("/{lgd_code}/physical-progress")
async def physical_progress(
    lgd_code: int,
    plan_year: int,
):
    return await get_panchayat_physical_progress(
        lgd_code=lgd_code,
        plan_year=plan_year,
    )