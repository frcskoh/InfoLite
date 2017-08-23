from bs4 import BeautifulSoup
import requests, re, json, asyncio, aiohttp, os

headers = {
    'Accept' : 'image/webp,image/apng,image/*,*/*;q=0.8', 
    'Accept-Encoding' : 'gzip, deflate', 
    'Accept-Language' : 'ja-JP,zh-CN;q=0.8,zh;q=0.6,ja;q=0.4,en-US;q=0.2,en;q=0.2', 
    'Host' : 'www.asahicom.jp', 
    'If-None-Match' : '"6fc2d6f-96b3-55766aa3da280"', 
    'Proxy-Connection' : 'keep-alive', 
    'Referer' : 'http//www.asahi.com/articles/ASK8R05N6K8QPTIL01T.html?iref=comtop_8_07', 
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    }

async def ArticleBuild(ID, session):
    global headers
    URL = 'http://www.asahi.com/articles/' + ID
    r = requests.session()
    async with session.get(URL) as resp:
        content = await resp.read()
        soup = BeautifulSoup(content, "lxml")
        try:
            title = soup.find('div', 'ArticleTitle').div
        except:
            print('None title. ')
            title_text = auth = update = None
        else:
            title_text = title.h1.get_text()
            auth = title.find('p', 'Sub').get_text() if title.find('p', 'Sub') else ""
            update = title.find('p', 'LastUpdated').get_text() if title.find('p', 'LastUpdated') else ""
      
        try: 
            body = soup.find('div', 'ArticleBody').div
        except:
            print('An article void. ')
            text = image = None
        else:
            if body.find('div', 'Image'):
                image = body.find('div', 'Image')
                if image.find('img'):
                    img_url = "".join(('http://', image.img['src'].strip('"').strip('/')))
                    main_image = os.path.join('static', 'cache', os.path.split(img_url)[-1])
                    if not os.path.exists(os.path.join('static', 'cache')):
                        os.makedirs(os.path.join('static', 'cache'))
                    for i in image.find_all('img'):
                        img_url = "".join(('http://', i['src'].strip('"').strip('/')))
                        write_path = os.path.join('static', 'cache', os.path.split(img_url)[-1])
                        try:
                            if not os.path.exists(write_path):
                                with open(write_path, 'wb') as f:
                                    f.write(r.get(img_url).content)
                            i['src'] = os.path.join('static', 'cache', write_path)
                            i['class'] = 'mdui-img-fluid'
                        except IOError:
                            print('Receive the image error ! ' + ID)
                        else:
                            print('Downloaded. ' + img_url)
                else:
                    main_image = None
            else:
                main_image = None
            
            text = "".join([str(i) for i in soup.find('div', 'ArticleText').find_all('p')])
            
    return {
            'title': title_text,
            'auth' : auth,
            'update' : update,
            'main_image' : main_image,
            'text' : text
            }

async def ContentMatch(part, session):
    t_info = {
        'ID' : part.a['href'].split('/articles/')[-1],
        'free' : True if part.find('img', "有料記事") else None, 
        'topic' : part['class']
        }
    t_info.update({'info' : await ArticleBuild(t_info['ID'], session)})
    
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
    while 1:
        try:
            soup = BeautifulSoup(requests.get(URLs).content, "lxml").find('ul', 'List')
            body = soup.find_all('li')[:-2]
##            print(body)
        except:
            print('Error. Retrying...')
        else:
            print('Received Successfully. ')
            break
    
    return SubProcess(body)

