from app import db

class Char(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    char_name = db.Column(db.String(50))
    char_class = db.Column(db.String(50))
    item_level = db.Column(db.Float)
    guild = db.Column(db.String(50))
    last_update = db.Column(db.DateTime)

    def __init__(self, char_name, last_update, char_class = "", item_level = 0, guild = ""):
        self.char_name = char_name
        self.char_class = char_class
        self.item_level = item_level
        self.guild = guild
        self.last_update = last_update