import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from scraper import scrape

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def run_scrape():
    scrape()


if __name__ == '__main__':
    manager.run()