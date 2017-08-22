from Receive import receive
from time import time as now_time

with open('data.pkl', 'wb') as f:
    pickle.dump(receive(), f)

with open('stamp.pkl', 'wb') as f:
    pickle.dump(now_time(), f)
