import os
from productor import Productor
from consumer import Consumer
import threading

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)
app.config['FLASK_ENV']='development'

print('1')
productor = Productor()
print('2')
consumer = Consumer()
threading.Thread(target=consumer.listen).start()
print('3')

@app.errorhandler(Exception)
def error_handler(e):
    consumer.errors.append(e)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    productor.send(name)
    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', names = consumer.names, errors = consumer.errors, partition = consumer.partition, event=consumer.event)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))
    
if __name__ == '__main__':
     app.run(debug=True)
   