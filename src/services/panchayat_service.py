from src.apis.egramswaraj import client

async def get_panchayat_planning(
    lgd_code: int,
    plan_year: int,
):
    return await client.get_planning_data(
        state_code=29,
        plan_year=plan_year,
        lgd_code=lgd_code,
    )