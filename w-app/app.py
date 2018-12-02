import os
from flask import Flask, redirect, url_for, request, render_template, current_app
from pymongo import MongoClient
from pymongo import DESCENDING

from flask_paginate import Pagination
from flask_basicauth import BasicAuth

from worker import celery
import celery.states as states

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'jaakko'
app.config['BASIC_AUTH_PASSWORD'] = 'wisdomtree'

basic_auth = BasicAuth(app)

client = MongoClient("db:27017")
db = client.wordsdb


@app.route('/')
def words():
    url = request.args.get('url', None)
    items = []
    if url:
        _items = db.wordsdb.find({'url': url}).sort([("count", DESCENDING)]).limit(100)
        items = [item for item in _items]

    return render_template('words.html', items=items)


@app.route('/reset', methods=['POST'])
def reset():

    db.drop_collection('wordsdb')
    return redirect(url_for('words'))


@app.route('/process_url', methods=['POST'])
def process_url():

    url = request.form['url']
    # TODO(jaakko): validate url

    task = celery.send_task('tasks.add', args=[url], kwargs={})
    return redirect(url_for('words', url=url))
    

@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


@app.route('/history')
@basic_auth.required
def history():

    total = db.wordsdb.find().count()
    page, per_page, offset = get_page_items()
    words = db.wordsdb.find().sort([("count", DESCENDING)]).skip(offset).limit(per_page)
    pagination = get_pagination(page=page,
        per_page=per_page,
        total=total,
        record_name=words,
    )
    
    return render_template('history.html', items=words, pagination=pagination)

def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap3')

def get_link_size():
    return current_app.config.get('LINK_SIZE', 'sm')

def show_single_page_or_not():
    return current_app.config.get('SHOW_SINGLE_PAGE', False)

def get_page_items():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page')
    if not per_page:
        per_page = current_app.config.get('PER_PAGE', 50)
    else:
        per_page = int(per_page)

    offset = (page - 1) * per_page
    return page, per_page, offset

def get_pagination(**kwargs):
       kwargs.setdefault('record_name', 'records')
       return Pagination(css_framework=get_css_framework(),
          link_size=get_link_size(),
          show_single_page=show_single_page_or_not(),
          **kwargs
          )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
