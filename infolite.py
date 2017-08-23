from flask import Flask, redirect
from flask_bootstrap import Bootstrap
from time import time as now_time
from receive import Receive
import _pickle as pickle

app = Flask(__name__)
bootstarp = Bootstrap(app)
#router
from flask import render_template, redirect, request
@app.route('/', methods = ['GET'])
def index():
    global data
    global stamp

    try:
        with open('stamp.pkl', 'rb+') as f:
            stamp = pickle.load(f)
            print('Cache Stamp : ' + str(stamp))
            if abs(stamp - now_time()) > 900:
                print('Old version found. Now is ' + str(now_time()) + '. ')
                data = Receive()
                with open('data.pkl', 'wb') as g:
                    g.seek(0)
                    g.truncate()
                    pickle.dump(data, g)
                stamp = now_time()
                f.seek(0)
                f.truncate()
                pickle.dump(stamp, f)
                print('Stamp updated : ' + str(stamp))
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
    
    return render_template('index.html', data = data, stamp = stamp, num = len(data))

@app.route('/articles/<order>', methods = ['GET'])
def articles(order):
    global data
    if not data:
        return redirect('/')
    else:
        return render_template('article.html', info = data[int(order)], order = int(order))
        
if __name__ == '__main__':
    app.run(debug = True)
