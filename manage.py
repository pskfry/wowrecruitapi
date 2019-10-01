import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from scraper import scrape
import sys

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def run_scrape(arg_min_ilvl):
    arg_min_ilvl = float(arg_min_ilvl)
    scrape(arg_min_ilvl)


if __name__ == '__main__':
    manager.run()