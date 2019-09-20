from app import db
from sqlalchemy.dialects.postgresql import JSON

class Char(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    char_name = db.Column(db.String(50))
    char_class = db.Column(db.String(50))
    item_level = db.Column(db.Float)
    guild = db.Column(db.String(50))
    last_update = db.Column(db.DateTime)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)