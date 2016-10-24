from flask_script import Manager as FlaskScriptManager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db)

manager = FlaskScriptManager(app)

from app.models import *
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
