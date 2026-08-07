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


async def get_panchayat_activities(
    lgd_code: int,
    plan_year: int,
):
    data = await get_panchayat_planning(
        lgd_code=lgd_code,
        plan_year=plan_year,
    )

    activities = []

    for item in data:
        activities.append({
            "activityCd": item.get("activityCd"),
            "activityType": item.get("activityType"),
            "activityName": item.get("activityName"),
            "totalCost": item.get("totalCost"),
            "schemeCodes": [
                f.get("schemeCode")
                for f in item.get("fundList", [])
                if f.get("schemeCode") is not None
            ],
            "activityStts": item.get("activityStts"),
        })

    return activities


async def get_panchayat_resource_envelope(
    lgd_code: int,
    plan_year: int,
):
    data = await get_panchayat_planning(
        lgd_code=lgd_code,
        plan_year=plan_year,
    )

    resources = []

    for item in data:
        for f in item.get("fundList", []):
            resources.append({
                "schemeCode": f.get("schemeCode"),
                "schemeComponentCode": f.get("componentCode"),
                "allocationAmountGen": (
                    (f.get("untiedAmountGen") or 0)
                    + (f.get("tiedAmountGen") or 0)
                ),
                "allocationAmountSc": (
                    (f.get("untiedAmountSc") or 0)
                    + (f.get("tiedAmountSc") or 0)
                ),
                "allocationAmountSt": (
                    (f.get("untiedAmountSt") or 0)
                    + (f.get("tiedAmountSt") or 0)
                ),
                "totalBudgetAmount": f.get("amountTotal"),
            })

    return resources


async def get_panchayat_physical_progress(
    lgd_code: int,
    plan_year: int,
):
    data = await get_panchayat_planning(
        lgd_code=lgd_code,
        plan_year=plan_year,
    )

    progress = []

    for item in data:
        asset = item.get("assetDetails")

        if asset and isinstance(asset, dict):
            locations = asset.get("assetLocationDetails") or []

            progress.append({
                "activityCd": item.get("activityCd"),
                "astLocType": (
                    str(locations[0].get("astLocCd"))
                    if locations
                    else None
                ),
                "astNm": asset.get("astNm"),
                "completed": None,
            })

    return progress


async def get_panchayat_dashboard(
    lgd_code: int,
    plan_year: int,
):
    data = await get_panchayat_planning(
        lgd_code=lgd_code,
        plan_year=plan_year,
    )

    activities = []
    resources = []
    progress = []

    for item in data:
        activities.append({
            "activityCd": item.get("activityCd"),
            "activityType": item.get("activityType"),
            "activityName": item.get("activityName"),
            "totalCost": item.get("totalCost"),
            "schemeCodes": [
                f.get("schemeCode")
                for f in item.get("fundList", [])
                if f.get("schemeCode") is not None
            ],
            "activityStts": item.get("activityStts"),
        })

        for f in item.get("fundList", []):
            resources.append({
                "schemeCode": f.get("schemeCode"),
                "schemeComponentCode": f.get("componentCode"),
                "allocationAmountGen": (
                    (f.get("untiedAmountGen") or 0)
                    + (f.get("tiedAmountGen") or 0)
                ),
                "allocationAmountSc": (
                    (f.get("untiedAmountSc") or 0)
                    + (f.get("tiedAmountSc") or 0)
                ),
                "allocationAmountSt": (
                    (f.get("untiedAmountSt") or 0)
                    + (f.get("tiedAmountSt") or 0)
                ),
                "totalBudgetAmount": f.get("amountTotal"),
            })

        asset = item.get("assetDetails")

        if asset and isinstance(asset, dict):
            locations = asset.get("assetLocationDetails") or []

            progress.append({
                "activityCd": item.get("activityCd"),
                "astLocType": (
                    str(locations[0].get("astLocCd"))
                    if locations
                    else None
                ),
                "astNm": asset.get("astNm"),
                "completed": None,
            })

    return {
        "activities": activities,
        "resources": resources,
        "progress": progress,
    }