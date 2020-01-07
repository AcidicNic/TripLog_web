from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/photos'

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/TripLog')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

logs = db.logs


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    ''' launch page '''
    return render_template('home.html')


@app.route('/begin')
def new_log():
    ''' new log form '''
    return render_template('begin_form.html')


@app.route('/create', methods=['POST'])
def new_log_submit():
    ''' adds the new log to the database and redirect to current_log '''
    now = datetime.now()
    log = {
        'title': request.form.get('title'),
        'desc': request.form.get('desc'),
        'dose': {
            'drug': request.form.get('drug'),
            'n': request.form.get('n'),
            # 'unit': request.form.get('unit')
        },
        'start_time': now.strftime('%-I:%M:%S %p'),
        'start_date': now.strftime('%b. %d, %Y'),
        'notes': []
    }
    log_id = logs.insert_one(log).inserted_id
    return redirect(url_for('log', log_id=log_id))


@app.route('/logs/<log_id>', methods=['POST'])
def add_note(log_id):
    ''' add updated info of a plant to the database and redirect to that plant's page '''
    now = datetime.now()
    note = request.form.get('note')
    log = logs.find_one({'_id': ObjectId(log_id)})
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            log['notes'].append({
                'type': 'img',
                'content': filename,
                'timestamp': now.strftime('%-I:%M:%S %p')
            })
    if not note == '':
        log['notes'].append({
            'type': 'str',
            'content': note,
            'timestamp': now.strftime('%-I:%M:%S %p')
        })
    logs.update_one(
        {'_id': ObjectId(log_id)},
        {'$set': log}
    )
    return redirect(url_for('log', log_id=log_id))


@app.route('/logs/<log_id>')
def log(log_id):
    '''  '''
    log = logs.find_one({'_id': ObjectId(log_id)})
    return render_template('current_log.html', log=log)


@app.route('/archive')
def archive():
    ''' archive '''
    return render_template('archive.html', logs=logs.find())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
