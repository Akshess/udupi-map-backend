from src.apis.egramswaraj import client

async def get_panchayat_planning(lgd_code: int, plan_year: int):
    return await client.get_planning_data(
        state_code=29,
        plan_year=plan_year,
        lgd_code=lgd_code,
    )

async def get_panchayat_activities(lgd_code: int, plan_year: int):
    data = await get_panchayat_planning(lgd_code=lgd_code, plan_year=plan_year)
    activities = []
    for item in data:
        activities.append({
            "activityCd": item.get("activityCd"),
            "activityType": item.get("activityType"),
            "activityName": item.get("activityName"),
            "totalCost": item.get("totalCost"),
            "schemeCode": (item.get("fundList") or [{}])[0].get("schemeCode"),
            "activityStts": item.get("activityStts"),
        })
    return activities

async def get_panchayat_resource_envelope(lgd_code: int, plan_year: int):
    data = await get_panchayat_planning(lgd_code=lgd_code, plan_year=plan_year)
    resources = []
    for item in data:
        for f in item.get("fundList", []):
            resources.append({
                "schemeCode": f.get("schemeCode"),
                "schemeComponentCode": f.get("componentCode"),
                "alocationAmountGen": f.get("untiedAmountGen") or f.get("tiedAmountGen") or 0,
                "alocationAmountSc": f.get("untiedAmountSc") or f.get("tiedAmountSc") or 0,
                "alocationAmountSt": f.get("untiedAmountSt") or f.get("tiedAmountSt") or 0,
                "totalBudjAmount": f.get("amountTotal"),
            })
    return resources

async def get_panchayat_physical_progress(lgd_code: int, plan_year: int):
    data = await get_panchayat_planning(lgd_code=lgd_code, plan_year=plan_year)
    progress = []
    for item in data:
        asset = item.get("assetDetails")
        if asset:
            astNm = asset.get("astNm") if isinstance(asset, dict) else None
            astLocType = None
            completed = None
            if isinstance(asset, dict):
                locs = asset.get("assetLocationDetails") or []
                if locs:
                    astLocType = str(locs[0].get("astLocCd"))
            progress.append({
                "activityCd": item.get("activityCd"),
                "astLocType": astLocType,
                "astNm": astNm,
                "completed": completed,
            })
    return progress
