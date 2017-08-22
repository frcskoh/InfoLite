from bs4 import BeautifulSoup
from stream import *
from multiprocessing import Pool, freeze_support
import json
from sys import setrecursionlimit
setrecursionlimit(1000000)

def Receive():
    freeze_support()
    data = None
    while not data:
        try:
            pool = Pool(processes = 1)
            result = [pool.apply_async(StreamUpdate, ()), ]
            pool.close()
            pool.join()
            data = json.loads(result[0].get())
        except:
            print('Retrying...')
            
    return data
