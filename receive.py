from stream import *
from multiprocessing import Pool, freeze_support
from sys import setrecursionlimit
import json
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
            print('Building the data...')
            data = json.loads(result[0].get())
        except:
            print('Retrying...')
            
    return data
