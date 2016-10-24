from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from config import APP_ENV

# Инициализация объекта приложения
app = Flask(__name__)

# Загрузка конфигурационных данных
app.config.from_object('config.{}Config'.format(APP_ENV))

# Debugger
if app.config.get('DEBUG'):
    toolbar = DebugToolbarExtension(app)

# Инициализация объекта БД
db = SQLAlchemy(app)


# Обработчик 404 ошибки
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Регистрация Blueprints
from app.blueprints.listings.views import listings
from app.blueprints.managers.views import managers
from app.blueprints.agents.views import agents
from app.blueprints.cities.views import cities
app.register_blueprint(listings)
app.register_blueprint(managers)
app.register_blueprint(agents)
app.register_blueprint(cities)
