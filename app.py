import os
import sys
from flask_sqlalchemy import SQLAlchemy
from flask import (jsonify, request, Response, abort, Flask, render_template)
import json

from sqlalchemy import inspect
from datetime import datetime

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

app = Flask(__name__, template_folder="templates")
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Char, Scrape

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
        try:
            req = request.get_json()
            charList = req["charList"]

            Char.query.delete()

            for char in charList:
                newChar = Char(char["charName"], char["lastUpdated"], "", char["itemLevel"], char["guildName"])
                db.session.add(newChar)

            new_row_count = Char.query.count()

            if new_row_count > 25:
                db.session.commit()
                return Response(status=200)
            else:
                db.session.rollback()
                abort(400)
        except:
            abort(400)

@app.route('/scrapelog', methods=['GET','POST'])
def scrape_log():
    if request.method == 'GET':
        scrapeList = Scrape.query.all()
        return json.dumps([object_as_dict(scrape) for scrape in scrapeList],default=str)

    if request.method == 'POST':
        try:
            req = request.get_json()
            newScrape = Scrape(req["scrapeStart"], req["scrapeEnd"], req["charCount"], req["minIlvl"], req["pagesScraped"])
            print(newScrape, file=sys.stderr)

            db.session.add(newScrape)
            db.session.commit()

            return Response(status=200)
        except:
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