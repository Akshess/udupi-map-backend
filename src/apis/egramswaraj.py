import httpx

class EGramSwarajClient:
    BASE_URL = "https://egramswaraj.gov.in/webservice"

    async def get_planning_data(
        self,
        state_code: int,
        plan_year: int,
        lgd_code: int,
    ):
        url = f"{self.BASE_URL}/getLbApprovedActivityData/{state_code}/{plan_year}/{lgd_code}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()


client = EGramSwarajClient()