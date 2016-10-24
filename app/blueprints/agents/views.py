from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from app import db
from app.models import Agent, City
from .forms import AgentForm

agents = Blueprint('agents', __name__)


@agents.route('/agents/')
def index():
    """Действие для отображения страницы со списком агентов."""
    return render_template('agents/index.html', agents=Agent.query.all())


@agents.route('/agents/create/', methods=['GET', 'POST'])
def create():
    """Действие для отображения страницы и создания агента."""
    form = AgentForm(request.form)
    form.city_id.choices = [(c.id, c.title) for c in City.query.order_by('title')]
    if request.method == 'POST' and form.validate():
        agent = Agent(name=form.name.data,
                      agency=form.agency.data,
                      phone_numbers=form.phone_numbers.data,
                      email=form.email.data,
                      city_id=form.city_id.data)
        db.session.add(agent)
        db.session.commit()
        flash('Agent added.')
        return redirect(url_for('agents.index'))
    return render_template('agents/create.html', form=form)


@agents.route('/agents/edit/<int:agent_id>/', methods=['GET', 'POST'])
def edit(agent_id):
    """Действие для отображения страницы и редактирования агента.

    :param agent_id: id агента в таблице *agents*
    :type agent_id: int
    """
    agent = Agent.query.get_or_404(agent_id)
    form = AgentForm(request.values, agent)
    form.city_id.choices = [(c.id, c.title) for c in City.query.order_by('title')]
    if request.method == 'POST' and form.validate():
        form.populate_obj(agent)
        db.session.commit()
        flash('Agent edited.')
        return redirect(url_for('agents.index'))
    return render_template('agents/edit.html', form=form)


@agents.route('/agents/delete/<int:agent_id>/')
def delete(agent_id):
    """Действие для удаления агента.

    :param agent_id: id агента в таблице *agents*
    :type agent_id: int
    """
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    flash('Agent deleted.')
    return redirect(url_for('agents.index'))


@agents.route('/agents/agencies.json/')
def get_agencies():
    """Возвращает json с названиями агенств (поле *agents.agency*).
    Используется для автоподсказок в форме создания/редактирования агента.

    :return: json
    """
    agencies = [m.agency
                for m in Agent.query.with_entities(Agent.agency).order_by(Agent.agency).all()
                if m.agency != '' and m.agency is not None]
    return jsonify(agencies)


@agents.route('/agents/names.json/<int:city_id>/')
def get_names(city_id):
    """Возвращает json с именами агентов (поле *agents.name*) в городе *city_id*.
    Используется для автоподсказок в форме создания/редактирования листинга.

    :param city_id: Идентификатор города в таблице *cities*.
    :return: json
    """
    names = [m.name
             for m in Agent.query.with_entities(Agent.name).distinct(Agent.name)
             .filter(Agent.city_id == city_id).order_by(Agent.name).all()
             if m.name != '' and m.name is not None]
    return jsonify(names)


@agents.route('/agents/phones.json/<int:city_id>/')
def get_phones(city_id):
    """Возвращает json с телефонами агентов (поле *agents.phone_numbers*) в городе *city_id*.
    Используется для автоподсказок в форме создания/редактирования листинга.

    :param city_id: Идентификатор города в таблице *cities*.
    :return: json
    """
    phones = [m.phone_numbers
              for m in Agent.query.with_entities(Agent.phone_numbers).distinct(Agent.phone_numbers)
              .filter(Agent.city_id == city_id).order_by(Agent.phone_numbers).all()
              if m.phone_numbers != '' and m.phone_numbers is not None]
    return jsonify(phones)


@agents.route('/agents/emails.json/<int:city_id>/')
def get_emails(city_id):
    """Возвращает json с email агентов (поле *agents.email*) в городе *city_id*.
    Используется для автоподсказок в форме создания/редактирования листинга.

    :param city_id: Идентификатор города в таблице *cities*.
    :return: json
    """
    emails = [m.email
              for m in Agent.query.with_entities(Agent.email).distinct(Agent.email)
              .filter(Agent.city_id == city_id).order_by(Agent.email).all()
              if m.email != '' and m.email is not None]
    return jsonify(emails)


@agents.route('/agents/get_agent_by_name/<agent_name>')
def get_agent_by_name(agent_name):
    """Возвращает json с данными агента, если он найден в БД по его имени.
    Используется для автозаполнения в форме создания/редактирования листинга.

    :param agent_name: Имя агента.
    :return: json
    """
    agent = Agent.query.filter_by(name=agent_name).first_or_404()
    return jsonify({
        'name': agent.name,
        'phone_numbers': agent.phone_numbers,
        'email': agent.email,
    })


@agents.route('/agents/get_agent_by_phone/<agent_phone>')
def get_agent_by_phone(agent_phone):
    """Возвращает json с данными агента, если он найден в БД по его телефону.
    Используется для автозаполнения в форме создания/редактирования листинга.

    :param agent_phone: Телефон агента.
    :return: json
    """
    agent = Agent.query.filter_by(phone_numbers=agent_phone).first_or_404()
    return jsonify({
        'name': agent.name,
        'phone_numbers': agent.phone_numbers,
        'email': agent.email,
    })


@agents.route('/agents/get_agent_by_email/<agent_email>')
def get_agent_by_email(agent_email):
    """Возвращает json с данными агента, если он найден в БД по его email.
    Используется для автозаполнения в форме создания/редактирования листинга.

    :param agent_email: Email агента.
    :return: json
    """
    agent = Agent.query.filter_by(email=agent_email).first_or_404()
    return jsonify({
        'name': agent.name,
        'phone_numbers': agent.phone_numbers,
        'email': agent.email,
    })
