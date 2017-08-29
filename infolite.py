from flask import Flask, redirect, abort, render_template
from time import time as now_time
import json
import _pickle as pickle
from flask_htmlmin import HTMLMIN

app = Flask(__name__)
app.config['MINIFY_PAGE'] = True
HTMLMIN(app)

#router
@app.route('/', methods = ['GET'])
def index():
    while 1:
        try:
            with open('stamp.pkl', 'rb') as f:
                stamp = pickle.load(f)
                print('Cache Stamp : %s' % (stamp))
                with open('data.pkl', 'rb') as f:
                    data = pickle.load(f)
                print('Read the data from cache. %s' % (stamp))
        except IOError:
            pass
        else:
            print('Received. The length is %s' % (len(data)))
            break
    return render_template('index.html', data = data, stamp = stamp, num = len(data))

@app.route('/articles/<order>', methods = ['GET'])
def articles(order):
    try:
        with open('data.pkl', 'rb') as f: data = pickle.load(f)
    except IOError:
        return redirect('/')
    else:
        print(str(order) + ' with ' + str(len(data)))
        return render_template('article.html', info = data[int(order)], order = int(order))

@app.route('/data/', methods = ['GET'])
def raw():
    try:
        with open('data.pkl', 'rb') as f: data = pickle.load(f)
        with open('stamp.pkl', 'rb') as f: stamp = pickle.load(f)
    except IOError:
        abort(404)
        return redirect('/')
    else:
        return json.dumps(
            {
                'stamp' : stamp, 
                'data' : data
            })

if __name__ == '__main__':
    app.run(debug = True)
