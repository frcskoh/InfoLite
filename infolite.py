from flask import Flask, redirect
from flask_bootstrap import Bootstrap
from time import time as now_time
from receive import Receive
import pickle

app = Flask(__name__)
bootstarp = Bootstrap(app)
data = None
stamp = 0

#router
from flask import render_template, redirect, request
@app.route('/', methods = ['GET'])
def index():
    global data
    global stamp

    try:
        with open('stamp.pkl', 'rb+') as f:
            stamp = pickle.load(f)
            print('Current Stamp : ' + str(stamp))
            if abs(stamp - now_time()) / 1000 > 900:
                print('Old version found. ')
                data = Receive()
                with open('data.pkl', 'wb') as g:
                    pickle.dump(data, g)
                stamp = now_time()
                pickle.dump(stamp, f)
                print('Stamp updated : ' + str(now_time()))
            else:
                with open('data.pkl', 'rb') as f:
                    data = pickle.load(f)
                print('Read the data from cache. ' + str(stamp))
    except IOError:
        print('stamp does not exist')
        data = Receive()
        with open('data.pkl', 'wb') as f:
            pickle.dump(data, f)
        stamp = now_time()
        with open('stamp.pkl', 'wb') as f:
            pickle.dump(stamp, f)
    
    return render_template('index.html', data = data, stamp = stamp)

@app.route('/articles/<order>', methods = ['GET'])
def articles(order):
    global data
    if not data:
        return redirect('/')
    else:
        return render_template('article.html', info = data[int(order)], order = int(order), num = len(data))
        
if __name__ == '__main__':
    app.run(debug = True)
