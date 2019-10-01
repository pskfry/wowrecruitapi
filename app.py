import os
import sys
import json
from flask_sqlalchemy import SQLAlchemy
from flask import (jsonify, request, Response, abort, Flask, render_template)
from sqlalchemy import inspect
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity, get_raw_jwt)
from datetime import datetime

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


app = Flask(__name__, template_folder="templates")

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

db = SQLAlchemy(app)
jwt = JWTManager(app)

from models import Char, Scrape, User


@app.route('/')
def home():
    return NotImplementedError


@app.route('/chars')
@jwt_required
def chars():
    page = 1 if request.args.get('page') is None else int(request.args.get('page'))
    limit = 20 if request.args.get('limit') is None else int(request.args.get('limit'))

    char_list = Char.query.paginate(page, limit, False).items
    res_body = {"char_list": []}

    res_body["char_list"].extend([object_as_dict(char) for char in char_list])
    return json.dumps(res_body, default=str)


@app.route('/char', methods=['GET','POST'])
@jwt_required
def char():
    if request.method == 'POST':
        try:
            req = request.get_json()
            print(req, file=sys.stderr)
            char_list = req["char_list"]

            Char.query.delete()

            for char in char_list:
                new_char = Char(char["char_name"], char["last_updated"], char["char_class"], char["item_level"], char["guild"])
                db.session.add(new_char)

            new_row_count = Char.query.count()

            if new_row_count > 25:
                db.session.commit()
                return Response(status=200)
            else:
                db.session.rollback()
            return Response(status=400)
        except:
            return Response(status=400)


@app.route('/scrapelog', methods=['GET','POST'])
@jwt_required
def scrape_log():
    if request.method == 'GET':
        scrape_list = Scrape.query.all()
        return Response(response=json.dumps([object_as_dict(scrape) for scrape in scrape_list],default=str), status=200, mimetype="application/json")

    if request.method == 'POST':
        try:
            print("hi")
            req = request.get_json()
            new_scrape = Scrape(
                req["scrape_start"], req["scrape_end"], req["char_count"], 
                req["min_ilvl"], req["pages_scraped"]
            )

            db.session.add(new_scrape)
            db.session.commit()

            return Response(status=200)
        except:
            return Response(status=400)


@app.route('/char/<int:char_id>')
def show_char(char_id):
    return 'here is the info for char with id %s' % char_id


@app.route('/login', methods=['POST'])
def login():
    try:
        req = request.json
        user = User.find_by_username(req["user_name"])

        if not user:
            return Response(response="get pooped on retard", status=400)

        user_verified = user.verify_hash(req["password"], user.password)

        if user_verified:
            access_token = create_access_token(identity = req["user_name"])
            res_body = {"access_token": access_token}
            
            return Response(response=json.dumps(res_body), mimetype="application/json", status=201)
        else:
            return Response(response="fuck u idiot", status=401)

    except ValueError as err:
        return Response(response="{0}".format(err), status=400)


@app.route('/register', methods=['POST'])
def register():
    try:
        req = request.get_json()
        if User.find_by_username(req["user_name"]):
            return Response(status_code=400)

    except:
        return Response(status_code=400)


if __name__ == '__main__':
    app.run()