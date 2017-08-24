from flask import Flask, redirect
from time import time as now_time
import _pickle as pickle
from flask_htmlmin import HTMLMIN
from jac.contrib.flask import JAC

app = Flask(__name__)
#app.config['COMPRESSOR_DEBUG'] = app.config.get('DEBUG')
#app.config['COMPRESSOR_OUTPUT_DIR'] = './static'
#app.config['COMPRESSOR_STATIC_PREFIX'] = '/static'
app.config['MINIFY_PAGE'] = True
jac = JAC(app)
HTMLMIN(app)

stamp = 0
data = []
#router
from flask import render_template, redirect, request
@app.route('/', methods = ['GET'])
def index():
    global data
    global stamp

    while 1:
        try:
            with open('stamp.pkl', 'rb') as f:
                stamp = pickle.load(f)
                print('Cache Stamp : ' + str(stamp))
                with open('data.pkl', 'rb') as f:
                    data = pickle.load(f)
                print('Read the data from cache. ' + str(stamp))
        except IOError:
            pass
        else:
            print(len(data))
            break
    return render_template('index.html', data = data, stamp = stamp, num = len(data))

@app.route('/articles/<order>', methods = ['GET'])
def articles(order):
    global data
    if not data:
        with open('data.pkl', 'rb') as f:
            data = pickle.load(f)
    print(str(order) + ' with ' + str(len(data)))
    return render_template('article.html', info = data[int(order)], order = int(order))    
if __name__ == '__main__':
    app.run(debug = True)
