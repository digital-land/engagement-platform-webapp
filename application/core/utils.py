import httpx

async def makeRequest(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print
        return response.text