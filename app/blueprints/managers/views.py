from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify, Response
from app import db
from app.models import Manager, City
from .forms import ManagerForm

managers = Blueprint('managers', __name__)


@managers.route('/managers/')
def index():
    """Действие для отображения страницы со списком менеджеров."""
    return render_template('managers/index.html', managers=Manager.query.all())


@managers.route('/managers/create/', methods=['GET', 'POST'])
def create():
    """Действие для отображения страницы и создания менеджера."""
    form = ManagerForm(request.form)
    form.city_id.choices = [(c.id, c.title) for c in City.query.order_by('title')]
    if request.method == 'POST':
        if form.validate():
            manager = Manager(name=form.name.data,
                              agency=form.agency.data,
                              phone_numbers=form.phone_numbers.data,
                              email=form.email.data,
                              city_id=form.city_id.data)
            db.session.add(manager)
            db.session.commit()
            flash('Manager added.')
            if not request.is_xhr:
                return redirect(url_for('managers.index'))
            else:
                return jsonify({
                    'success': True
                })
        else:
            # Если есть ошибки валидации при AJAX-запросе
            if request.is_xhr:
                validation_errors = list()
                for field, errors in form.errors.items():
                    for error in errors:
                        validation_errors.append("Error in the %s field - %s <br>" % (
                            getattr(form, field).label.text,
                            error
                        ))
                return Response(response=validation_errors,
                                status=400,
                                mimetype="application/json")
    return render_template('managers/create.html', form=form)


@managers.route('/managers/edit/<int:manager_id>/', methods=['GET', 'POST'])
def edit(manager_id):
    """Действие для отображения страницы и редактирования менеджера.

    :param manager_id: id менеджера в таблице *managers*
    :type manager_id: int
    """
    manager = Manager.query.get_or_404(manager_id)
    form = ManagerForm(request.values, manager)
    form.city_id.choices = [(c.id, c.title) for c in City.query.order_by('title')]
    if request.method == 'POST' and form.validate():
        form.populate_obj(manager)
        db.session.commit()
        flash('Manager edited.')
        return redirect(url_for('managers.index'))
    return render_template('managers/edit.html', form=form)


@managers.route('/managers/delete/<int:manager_id>/')
def delete(manager_id):
    """Действие для удаления менеджера.

    :param manager_id: id менеджера в таблице *managers*
    :type manager_id: int
    """
    manager = Manager.query.get_or_404(manager_id)
    db.session.delete(manager)
    db.session.commit()
    flash('Manager deleted.')
    return redirect(url_for('managers.index'))


@managers.route('/managers/agencies.json/')
def get_agencies():
    """Возвращает json с названиями агенств (поле *managers.agency*).
    Используется для автоподсказок в форме создания/редактирования менеджера.

    :return: json
    """
    agencies = [m.agency
                for m in Manager.query.with_entities(Manager.agency).distinct(Manager.agency)
                .order_by(Manager.agency).all()
                if m.agency != '' and m.agency is not None]
    return jsonify(agencies)


@managers.route('/managers/names.json/<int:city_id>/')
def get_names(city_id):
    """Возвращает json с именами менеджеров (поле *managers.name*) в городе *city_id*.
    Используется для автоподсказок в форме создания/редактирования листинга.

    :param city_id: Идентификатор города в таблице *cities*.
    :return: json
    """
    names = [m.name
             for m in Manager.query.with_entities(Manager.name).distinct(Manager.name)
             .filter(Manager.city_id == city_id).order_by(Manager.name).all()
             if m.name != '' and m.name is not None]
    return jsonify(names)


@managers.route('/managers/get_manager_by_name/<string:manager_name>/<int:city_id>/')
def get_manager_by_name(manager_name, city_id):
    """Возвращает json с данными менеджера, если он найден в БД по его имени в городе city_id.
    Используется для проверки существует ли менеджер при отправке формы создания/редактирования листинга.

    :param manager_name: Имя агента.
    :param city_id: id города.
    :return: json
    """
    manager = Manager.query.filter_by(name=manager_name, city_id=city_id).first_or_404()
    return jsonify({
        'name': manager.name,
        'phone_numbers': manager.phone_numbers,
        'email': manager.email,
    })
