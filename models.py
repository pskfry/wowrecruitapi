from app import db
from datetime import datetime
from dateutil.parser import parse


class Char(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    char_name = db.Column(db.String(50))
    char_class = db.Column(db.String(50))
    item_level = db.Column(db.Float)
    guild = db.Column(db.String(50))
    last_update = db.Column(db.DateTime)

    def __init__(self, char_name, last_update, char_class="", item_level=0, guild=""):
        self.char_name = char_name
        self.char_class = char_class
        self.item_level = item_level
        self.guild = guild
        self.last_update = last_update


class Scrape(db.Model):
    __tablename__ = 'scrape_log'
    id = db.Column(db.Integer, primary_key=True)
    scrape_start = db.Column(db.DateTime)
    scrape_end = db.Column(db.DateTime)
    char_count = db.Column(db.Integer)
    min_ilvl = db.Column(db.Float)
    pages_scraped = db.Column(db.Integer)

    def __init__(self, scrape_start, scrape_end, char_count=0, min_ilvl=0, pages_scraped=0):
        scrape_start = parse(scrape_start)
        scrape_end = parse(scrape_end)
        self.scrape_start = scrape_start
        self.scrape_end = scrape_end
        self.char_count = char_count
        self.min_ilvl = min_ilvl
        self.pages_scraped = pages_scraped

    def __repr__(self):
        return "started at %s ended at %s char count %s min ilv %s, %s pages scraped" % (
            self.scrape_start, self.scrape_end, self.char_count, self.min_ilvl, self.pages_scraped)
