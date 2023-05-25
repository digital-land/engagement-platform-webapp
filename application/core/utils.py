import json
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

cmsDomain = os.getenv("CMS_URL", "http://localhost:8000/")

print(cmsDomain)

pagesUrl = cmsDomain + "api/v2/pages/?format=json"

cmsUrl = cmsDomain + "api/v2/pages/{0}/?format=json"

async def makeRequest(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
        except Exception as e:
            raise('Couldn\'t make request to: ' + url + ' Reason: ' + e)
        return response.text




async def getPageContent(pageId):
    url = cmsUrl.format(pageId)
    print('making request to: ' + url)
    try:
        response = await makeRequest(url)
    except Exception as e:
        raise('Couldn\'t get page content for page id' + pageId + ' Reason: ' + e)
    return json.loads(response)


async def getPageApiFromTitle(title):
    pageId = None
    async with httpx.AsyncClient() as client:
        try:
            pagesResponse = await client.get(pagesUrl)
        except Exception as e:
            raise Exception("Can't connect to cms, " + e)
        pages = pagesResponse.json()
        for page in pages["items"]:
            if page["title"] == title:
                pageId = page["id"]
                break
    if(pageId == None):
        raise Exception('No page found in cms with title: ' + title)
    else:
        return await getPageContent(pageId)
