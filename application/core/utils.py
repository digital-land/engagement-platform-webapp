import json
import httpx

pagesUrl = 'http://localhost:8000/api/v2/pages/?format=json'

async def makeRequest(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
    
    
cmsUrl = "http://localhost:8000/api/v2/pages/{0}/?format=json"

async def getPageContent(pageId):
    url = cmsUrl.format(pageId)
    response = await makeRequest(url)
    return json.loads(response)
    

async def getPageApiFromTitle(title):
    async with httpx.AsyncClient() as client:
        pagesResponse = await client.get(pagesUrl)
        pages = pagesResponse.json()
        for page in pages['items']:
            if(page['title'] == title):
                pageId = page['id']
                break
    return await getPageContent(pageId)
