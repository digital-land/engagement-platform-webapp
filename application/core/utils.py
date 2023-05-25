import json
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

cmsDomain = os.getenv("CMS_URL", "http://localhost:8002/")

print(cmsDomain)

pagesUrl = cmsDomain + "api/v2/pages/?format=json"

cmsUrl = cmsDomain + "api/v2/pages/{0}/?format=json"

async def makeRequest(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text




async def getPageContent(pageId):
    url = cmsUrl.format(pageId)
    print('making request to: ' + url)
    response = await makeRequest(url)
    return json.loads(response)


async def getPageApiFromTitle(title):
    async with httpx.AsyncClient() as client:
        pagesResponse = await client.get(pagesUrl)
        pages = pagesResponse.json()
        for page in pages["items"]:
            if page["title"] == title:
                pageId = page["id"]
                break
    return await getPageContent(pageId)
