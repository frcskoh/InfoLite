from bs4 import BeautifulSoup
import requests, re, json, asyncio, aiohttp
from multiprocessing import Pool, freeze_support
from sys import setrecursionlimit

async def ArticleBuild(ID, session):
    URL = 'http://www.asahi.com/articles/' + ID
    async with session.get(URL) as resp:
        content = await resp.read()
        soup = BeautifulSoup(content, "lxml")
        title = soup.find('div', 'ArticleTitle').div

        title_text = title.h1.get_text()
        auth = title.find('p', 'Sub').get_text() if title.find('p', 'Sub') else ""
        update = title.find('p', 'LastUpdated').get_text() if title.find('p', 'LastUpdated') else ""
    
        body = soup.find('div', 'ArticleBody').div

        if body.find('div', 'Image'):
            image = body.find('div', 'Image')
            if image.find('img'):
                image = image.img['src'].strip('"')
            else:
                image = None
        else:
            image = None
        text = "".join([str(i) for i in soup.find('div', 'ArticleText').find_all('p')])

    return {
            'title': title_text,
            'auth' : auth,
            'update' : update,
            'image' : image,
            'text' : text
            }

async def ContentMatch(part, session):
    t_info = {
        'ID' : part.a['href'].split('/articles/')[-1],
        'title' : re.sub('\(.*\)', '', re.match('.*\(.*\)', part.get_text()).group()),
        'date' : re.search('\(.*\)', re.match('.*\(.*\)', part.get_text()).group()).group().lstrip('(').rstrip(')')
        }
    t_info.update({'info' : await ArticleBuild(t_info['ID'], session)})
    #print(t_info)
    return t_info

def SubProcess(body):
    session = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(ContentMatch(i, session)) for i in body]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    session.close()
    
    return json.dumps([i.result() for i in tasks])
    
def StreamUpdate():
    URLs = 'http://www.asahi.com/news/'
    soup = BeautifulSoup(requests.get(URLs).content, "lxml").find('ul', 'List')
    body = soup.find_all('li')[:-2]
    
    return SubProcess(body)

