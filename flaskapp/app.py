from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import os
import json
import requests
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
    # r = requests.get('http://tripbot.tripsit.me/api/tripsit/getAllDrugAliases')
    # drug_list = r.json()['data'][0]

    # with open('static/drug_list.txt') as json_file:
    #     drug_list = json.load(json_file)
    # util = {
    #     'drug_list': list(drug_list)
    # }
    log={}
    return render_template('begin_form.html', log=log)


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
    username = request.form.get('username')
    if desc == '':
        desc = 'write a description!'
    if username == '':
        username = 'username'
    if title == '':
        title = f"{username}'s Experience"
    log = {
        'username': username,
        'start_time': now.strftime('%-I:%M:%S %p'),
        'start_date': now.strftime('%b. %d, %Y'),
        'title': title,
        'desc': desc,
        'doses': [],
        'notes': [],
        'status': 'CURRENTLY_TRIPPING'
    }

    drugs = request.form.getlist('drug')
    doses = request.form.getlist('dose')
    units = request.form.getlist('unit')
    for i in range(len(drugs)):
        if drugs[i] != '':
            log['doses'].append(get_drug_info(drugs[i], doses[i], units[i]))
    log['notes'].append({
        'id': 0,
        'type': 'hidden',
        'content': 'Log Started',
        'timestamp': now.strftime('%-I:%M:%S %p'),
        'edits': []
    })
    # if request.form.get('currently_tripping'):
    #     log['status'] = 'CURRENTLY_TRIPPING'
    log_id = logs.insert_one(log).inserted_id
    return redirect(url_for('log', log_id=log_id))


@app.route('/logs/<log_id>', methods=['POST'])
def update(log_id):
    ''' add updated info to the database '''
    # Add Dose
    if request.form["update_btn"] == "add_dose":
        return add_dose(log_id)
    # Change Status
    elif request.form["update_btn"] == "status":
        return change_status(log_id)
    # Edit Title/Description
    elif request.form["update_btn"] == "edit_desc":
        return update_desc(log_id)
    # Edit Note
    elif request.form["update_btn"] == "edit_note":
        return edit_note(log_id)
    # Add Note
    else:
        return add_note(log_id)


def edit_note(log_id):
    now = datetime.now()
    note_index = request.form.get('note_id')
    addon = request.form['addon']
    # addon = request.form.get('addon')
    log = logs.find_one({'_id': ObjectId(log_id)})

    log['notes'][int(note_index)]['edits'].append({
        'id': len(log['notes'][int(note_index)]['edits']),
        'type': 'str',
        'content': addon,
        'timestamp': now.strftime('%-I:%M:%S %p'),
    })
    logs.update_one(
        {'_id': ObjectId(log_id)},
        {'$set': log}
    )
    return redirect(url_for('log', log_id=log_id))


def add_note(log_id):
    now = datetime.now()
    note = request.form.get('note')
    log = logs.find_one({'_id': ObjectId(log_id)})
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            log['notes'].append({
                'id': log['notes'][-1]['id']+1,
                'type': 'img',
                'content': filename,
                'timestamp': now.strftime('%-I:%M:%S %p'),
                'edits': []
            })
    if not note == '':
        if note[:4] == '??? ':
            log['notes'].append({
                'id': log['notes'][-1]['id']+1,
                'type': 'question',
                'content': note,
                'timestamp': now.strftime('%-I:%M:%S %p'),
                'edits': []
            })
            log['notes'].append({
                'id': log['notes'][-1]['id']+1,
                'type': 'answer',
                'content': ask_the_caterpillar(note[4:]),
                'timestamp': now.strftime('%-I:%M:%S %p'),
                'edits': []
            })
        else:
            log['notes'].append({
                'id': log['notes'][-1]['id']+1,
                'type': 'str',
                'content': note,
                'timestamp': now.strftime('%-I:%M:%S %p'),
                'edits': []
            })
    logs.update_one(
        {'_id': ObjectId(log_id)},
        {'$set': log}
    )
    return redirect(url_for('log', log_id=log_id))


def update_desc(log_id):
    now = datetime.now()
    log = logs.find_one({'_id': ObjectId(log_id)})
    desc = request.form.get('desc')
    title = request.form.get('title')
    if desc == '':
        desc = 'write a description!'
    if title == '':
        title = f"{log['username']}'s Experience"
    if desc == log['desc'] and title == log['title']:
        return redirect(url_for('log', log_id=log_id))
    if title != log['title']:
        log['notes'].append({
            'id': log['notes'][-1]['id']+1,
            'type': 'hidden',
            'content': f"The title has been changed from \"{log['title']}\" to \"{title}\"",
            'timestamp': now.strftime('%-I:%M:%S %p'),
            'edits': []
        })
    if desc != log['desc']:
        log['notes'].append({
            'id': log['notes'][-1]['id']+1,
            'type': 'hidden',
            'content': f"The description has been changed from \"{log['desc']}\" to \"{desc}\"",
            'timestamp': now.strftime('%-I:%M:%S %p'),
            'edits': []
        })
    log['title'] = title
    log['desc'] = desc
    logs.update_one(
        {'_id': ObjectId(log_id)},
        {'$set': log}
    )
    return redirect(url_for('log', log_id=log_id))


def change_status(log_id):
    ''' change the status of a log. '''
    now = datetime.now()
    log = logs.find_one({'_id': ObjectId(log_id)})

    if log['status'] != 'COMPLETED':
        log['status'] = 'COMPLETED'
        log['notes'].append({
            'id': log['notes'][-1]['id']+1,
            'type': 'str',
            'content': 'This log was marked completed.',
            'timestamp': now.strftime('%-I:%M:%S %p'),
            'edits': []
        })
    else:
        log['status'] = 'CURRENTLY_TRIPPING'
        log['notes'].append({
            'id': log['notes'][-1]['id']+1,
            'type': 'str',
            'content': 'This log was reopened.',
            'timestamp': now.strftime('%-I:%M:%S %p'),
            'edits': []
        })
    logs.update_one(
        {'_id': ObjectId(log_id)},
        {'$set': log}
    )
    return redirect(url_for('log', log_id=log_id))


def add_dose(log_id):
    ''' updates the log and redirect to current_log '''
    log = logs.find_one({'_id': ObjectId(log_id)})
    now = datetime.now()
    drug = request.form.get('drug')
    dose = request.form.get('dose')
    unit = request.form.get('unit')
    if drug != '':
        log['doses'].append(get_drug_info(drug, dose, unit))
        log['notes'].append({
            'id': log['notes'][-1]['id']+1,
            'type': 'str',
            'content': f"Dose Added. {dose}{unit} of {drug}",
            'timestamp': now.strftime('%-I:%M:%S %p'),
            'edits': []
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


@app.route('/logs/<log_id>/edit')
def edit_log(log_id):
    ''' form to edit a log's information '''
    log = logs.find_one({'_id': ObjectId(log_id)})
    return render_template('log_edit_form.html', log=log)


@app.route('/logs/<log_id>/update', methods=['POST'])
def update_log(log_id):
    ''' add updated info to the database and redirect to that log's page '''
    log = logs.find_one({'_id': ObjectId(log_id)})
    now = datetime.now()
    desc = request.form.get('desc')
    title = request.form.get('title')
    if desc == '':
        log['desc'] = 'write a description!'
    if title == '':
        log['title'] = f"{log['username']}'s Experience"

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


def ask_the_caterpillar(query):
    r = requests.post('https://www.askthecaterpillar.com/query', {"query": query})
    if r.status_code == 200:
        data = r.json()
        return data["data"]["messages"][0]["content"]
    return f"So sorry! Ask The Caterpillar is currently down, try again later. (Error {r.status_code}: {r.reason})"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 666))
