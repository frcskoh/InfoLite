from stream import StreamUpdate
from time import time as now_time
import json
import _pickle as pickle

while 1:
    try:
        data = json.loads(StreamUpdate())
        with open('stamp.pkl', 'wb') as f: pickle.dump(now_time(), f)
        with open('data.pkl', 'wb') as f: pickle.dump(data, f)
    except:
        print('Error . Retrying...')
    else:
        print('Updated Successfully. ')
        break
