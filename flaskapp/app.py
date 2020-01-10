from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import os
import json
import requests
from werkzeug.utils import secure_filename
from pysychonaut import AskTheCaterpillar

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
    # r = requests.get('http://tripbot.tripsit.me/api/tripsit/getAllDrugAliases')
    # drug_list = r.json()['data'][0]

    with open('static/drug_list.txt') as json_file:
        drug_list = json.load(json_file)
    util = {
        'drug_list': list(drug_list)
    }
    log={}
    return render_template('begin_form.html', UTIL=util, log=log)




def get_drug_info(drug_name, dose, unit):
    r = requests.get(f'http://tripbot.tripsit.me/api/tripsit/getDrug', params={'name': drug_name}).json()
    if dose == '':
        dose = '?'
    if unit == '':
        unit = '?'
    if r['err'] is not None:
        return {
            'drug': drug_name,
            'dose': dose,
            'unit': unit,
        }
    drug = r['data'][0]
    drug_dict = {
        'drug': drug_name,
        'dose': dose,
        'unit': unit,
        'info': drug['properties'],
        'effects': []
    }
    print(drug['properties'])
    effects = drug['formatted_effects']
    for effect in effects:
        if effect != '':
            drug_dict['effects'].append(effect)
    if drug_name != drug['pretty_name']:
        drug_dict['pretty_name'] = drug['pretty_name']
    return drug_dict



@app.route('/create', methods=['POST'])
def new_log_submit():
    ''' adds the new log to the database and redirect to current_log '''
    now = datetime.now()
    desc = request.form.get('desc')
    title = request.form.get('title')
    if desc == '':
        desc = 'write a description!'
    if title == '':
        title = "testname's Experience"
    log = {
        'username': 'testname',
        'start_time': now.strftime('%-I:%M:%S %p'),
        'start_date': now.strftime('%b. %d, %Y'),
        'title': title,
        'desc': desc,
        'doses': [],
        'notes': [],
    }

    drugs = request.form.getlist('drug')
    doses = request.form.getlist('dose')
    units = request.form.getlist('unit')
    for i in range(len(drugs)):
        if drugs[i] != '':
            log['doses'].append(get_drug_info(drugs[i], doses[i], units[i]))
    if request.form.get('currently_tripping'):
        log['status'] = 'CURRENTLY_TRIPPING'
    log_id = logs.insert_one(log).inserted_id
    return redirect(url_for('log', log_id=log_id))


@app.route('/logs/<log_id>', methods=['POST'])
def add_note(log_id):
    ''' add updated info to the database '''
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
        print(note[:3])
        log['notes'].append({
            'type': 'str',
            'content': note,
            'timestamp': now.strftime('%-I:%M:%S %p')
        })
        if note[:4] == '??? ':log['notes'].append({
            'type': 'answer',
            'content': AskTheCaterpillar.ask_the_caterpillar(note[4:]),
            'timestamp': now.strftime('%-I:%M:%S %p')
        })
    logs.update_one(
        {'_id': ObjectId(log_id)},
        {'$set': log}
    )
    return redirect(url_for('log', log_id=log_id))


@app.route('/logs/<log_id>', methods=['POST'])
def change_status(log_id):
    ''' change the status of a log. '''
    now = datetime.now()
    log = logs.find_one({'_id': ObjectId(log_id)})

    log['notes'].append({
        'type': 'str',
        'content': 'This log was marked completed.',
        'timestamp': now.strftime('%-I:%M:%S %p')
    })
    log['status'] = 'COMPLETED'
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


@app.route('/logs/<log_id>/edit')
def edit_log(log_id):
    ''' form to edit a log's information '''
    log = logs.find_one({'_id': ObjectId(log_id)})
    return render_template('log_edit_form.html', log=log)


@app.route('/logs/<log_id>', methods=['POST'])
def update_log(log_id):
    ''' add updated info to the database and redirect to that log's page '''
    log = logs.find_one({'_id': ObjectId(log_id)})
    now = datetime.now()
    desc = request.form.get('desc')
    title = request.form.get('title')
    if desc == '':
        log['desc'] = 'write a description!'
    if title == '':
        log['title'] = "testname's Experience"

    log['doses'] = []
    drugs = request.form.getlist('drug')
    doses = request.form.getlist('dose')
    units = request.form.getlist('unit')
    for i in range(len(drugs)):
        if drugs[i] != '':
            log['doses'].append(get_drug_info(drugs[i], doses[i], units[i]))

    logs.update_one(
        {'_id': ObjectId(log_id)},
        {'$set': log})
    return redirect(url_for('log', log_id=log_id))


@app.route('/logs/<log_id>/delete', methods=['POST'])
def delete_log(log_id):
    ''' delete a log and redirect to <where> '''
    logs.delete_one({'_id': ObjectId(log_id)})
    return redirect(url_for('archive'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 666))
