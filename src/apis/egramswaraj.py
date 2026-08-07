import httpx


class EGramSwarajClient:
    BASE_URL = "https://egramswaraj.gov.in/webservice"

    async def get_planning_data(
        self,
        state_code: int,
        plan_year: int,
        lgd_code: int,
    ):
        url = (
            f"{self.BASE_URL}/"
            f"getLbApprovedActivityData/"
            f"{state_code}/{plan_year}/{lgd_code}"
        )

        timeout = httpx.Timeout(
            connect=10.0,
            read=60.0,
            write=10.0,
            pool=10.0,
        )

        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()

            return response.json()


client = EGramSwarajClient()