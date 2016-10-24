from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import City
from .forms import CityForm

cities = Blueprint('cities', __name__)


@cities.route('/cities/')
def index():
    """Действие для отображения страницы со списком городов."""
    return render_template('cities/index.html', cities=City.query.all())


@cities.route('/cities/create', methods=['GET', 'POST'])
def create():
    """Действие для отображения страницы и создания города."""
    form = CityForm(request.form)
    if request.method == 'POST' and form.validate():
        city = City(title=form.title.data)
        db.session.add(city)
        db.session.commit()
        flash('City added.')
        return redirect(url_for('cities.index'))
    return render_template('cities/create.html', form=form)


@cities.route('/cities/edit/<int:city_id>', methods=['GET', 'POST'])
def edit(city_id):
    """Действие для отображения страницы и редактирования города.

    :param city_id: id города в таблице *cities*
    :type city_id: int
    """
    city = City.query.get_or_404(city_id)
    form = CityForm(request.values, city)
    if request.method == 'POST' and form.validate():
        form.populate_obj(city)
        db.session.commit()
        flash('City edited.')
        return redirect(url_for('cities.index'))
    return render_template('cities/edit.html', form=form)


@cities.route('/cities/delete/<int:city_id>')
def delete(city_id):
    """Действие для удаления гогрода.

    :param city_id: id города в таблице *cities*
    :type city_id: int
    """
    city = City.query.get_or_404(city_id)
    db.session.delete(city)
    db.session.commit()
    flash('City deleted.')
    return redirect(url_for('cities.index'))
