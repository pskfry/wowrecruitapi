import os
from flask_sqlalchemy import SQLAlchemy
from flask import (jsonify, request, Response, abort, Flask, render_template)
import json

from sqlalchemy import inspect

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

app = Flask(__name__, template_folder="templates")
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Char

@app.route('/')
def home():
    """
    index response
    """
    charList = Char.query.all()
    return render_template('home.html', charList=charList)

@app.route('/chars')
def chars():
    charList = Char.query.all()
    return json.dumps([object_as_dict(char) for char in charList],default=str)

@app.route('/char', methods=['GET','POST'])
def char():
    if request.method == 'POST':
        if request.is_json:
            req = request.get_json()
            charList = req["charList"]
            for char in charList:
                newChar = Char(char["charName"], char["lastUpdated"])
                db.session.add(newChar)
            db.session.commit()
            return Response(status=200)
        else:
            abort(400)
        

@app.route('/char/<int:charId>')
def show_char(charId):
    return 'here is the info for char with id %s' % charId

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'logging ya in'
    else:
        return 'heres a login form'


if __name__ == '__main__':
    app.run()