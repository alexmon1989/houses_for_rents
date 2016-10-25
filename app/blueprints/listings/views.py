from flask import Blueprint, render_template, jsonify, request, url_for, flash, redirect
from sqlalchemy import or_
from app import db
from app.models import Listing, Manager, Agent, City
from datatables import ColumnDT, DataTables
from datetime import datetime
from .forms import ListingForm

listings = Blueprint('listings', __name__)


@listings.route('/')
@listings.route('/listings/')
def index():
    """Действие для отображения страницы со списком листингов."""
    return render_template('listings/index.html')


@listings.route('/listings/show/<int:listing_id>')
def show(listing_id):
    """Действие для отображения страницы отображения деталей листинга."""
    return render_template('listings/show.html', listing=Listing.query.get_or_404(listing_id))


@listings.route('/listings/create/', methods=['GET', 'POST'])
def create():
    """Действие для отображения страницы и создания листинга."""
    form = ListingForm(request.form)
    form.city_id.choices = [(c.id, c.title) for c in City.query.order_by('title')]
    if request.method == 'POST' and form.validate():
        # Получение agent по введенным реквизитам
        agent_id = None
        if form.agent_name.data:
            agent = Agent.query.filter(Agent.name == form.agent_name.data,
                                       or_(Agent.email == form.agent_email.data,
                                           Agent.phone_numbers == form.agent_phone.data)).first()
            if agent:
                # Если агент существует в БД, то получение его id
                agent_id = agent.id
                if form.agent_email.data != '' and agent.email != form.agent_email.data:
                    agent.email = form.agent_email.data
                if form.agent_phone.data != '' and agent.phone_numbers != form.agent_phone.data:
                    agent.phone_numbers = form.agent_phone.data
                db.session.commit()
            else:
                # Создание agent
                agent = Agent(name=form.agent_name.data,
                              email=form.agent_email.data,
                              phone_numbers=form.agent_phone.data,
                              city_id=form.city_id.data)
                db.session.add(agent)
                db.session.commit()
                agent_id = agent.id

        # Получение manager_id
        manager_id = None
        if form.appraised_by.data:
            manager = Manager.query.filter_by(name=form.appraised_by.data).first()
            manager_id = manager.id

        # Создание и созранение листинга
        listing = Listing(street_number=form.street_number.data,
                          street_address=form.street_address.data,
                          suburb=form.suburb.data,
                          property_type=form.property_type.data,
                          bedrooms=form.bedrooms.data,
                          government_value=form.government_value.data,
                          current_rates=form.current_rates.data,
                          median_rent_qv=form.median_rent_qv.data,
                          capital_growth=form.capital_growth.data,
                          median_rent_tb=form.median_rent_tb.data,
                          city_id=form.city_id.data,
                          agent_id=agent_id,
                          manager_id=manager_id)
        db.session.add(listing)
        db.session.commit()
        flash('Listing added.')
        return redirect(url_for('listings.index'))
    return render_template('listings/create.html', form=form)


@listings.route('/listings/edit/<int:listing_id>', methods=['GET', 'POST'])
def edit(listing_id):
    """Действие для отображения страницы и редактирования листинга.

    :param listing_id: id листинга в таблице *listings*
    :type listing_id: int
    """
    listing = Listing.query.get_or_404(listing_id)
    form = ListingForm(request.form, listing, data={
        'agent_name': listing.agent.name,
        'agent_phone': listing.agent.phone_numbers,
        'agent_email': listing.agent.email,
        'appraised_by': listing.manager.name,
    })
    form.city_id.choices = [(c.id, c.title) for c in City.query.order_by('title')]
    if request.method == 'POST' and form.validate():
        # Получение agent по введенным реквизитам
        agent = Agent.query.filter(Agent.name == form.agent_name.data,
                                   or_(Agent.email == form.agent_email.data,
                                       Agent.phone_numbers == form.agent_phone.data)).first()
        if agent:
            # Если агент существует в БД, то получение его id
            agent_id = agent.id
            if form.agent_email.data != '' and agent.email != form.agent_email.data:
                agent.email = form.agent_email.data
            if form.agent_phone.data != '' and agent.phone_numbers != form.agent_phone.data:
                agent.phone_numbers = form.agent_phone.data
            db.session.commit()
        else:
            # Создание agent
            agent = Agent(name=form.agent_name.data,
                          email=form.agent_email.data,
                          phone_numbers=form.agent_phone.data,
                          city_id=form.city_id.data)
            db.session.add(agent)
            db.session.commit()
            agent_id = agent.id

        # Получение manager_id
        manager = Manager.query.filter_by(name=form.appraised_by.data).first()
        manager_id = manager.id

        # Заполнение listing значениями формы и сохранение
        form.populate_obj(listing)
        listing.agent_id = agent_id
        listing.manager_id = manager_id
        db.session.commit()
        flash('Listing edited.')
        return redirect(url_for('listings.index'))
    return render_template('listings/edit.html', form=form)


@listings.route('/listings/delete/<int:listing_id>')
def delete(listing_id):
    """Действие для удаления листинга.

    :param listing_id: id листинга в таблице *listings*
    :type listing_id: int
    """
    listing = Listing.query.get_or_404(listing_id)
    db.session.delete(listing)
    db.session.commit()
    flash('Listing deleted.')
    return redirect(url_for('listings.index'))


@listings.route('/listings/data/')
def data():
    """Возвращает данные для Jquery DataTables."""
    # Поля для таблицы
    columns = list()
    columns.append(ColumnDT('id'))
    columns.append(ColumnDT('city.title'))
    columns.append(ColumnDT('street_address'))
    columns.append(ColumnDT('street_number'))
    columns.append(ColumnDT('suburb'))
    columns.append(ColumnDT('bedrooms'))
    columns.append(ColumnDT('agent.name'))
    columns.append(ColumnDT('agent.phone_numbers'))
    columns.append(ColumnDT('government_value'))
    columns.append(ColumnDT('updated_at'))
    columns.append(ColumnDT('created_at'))

    # Инициализация запроса
    query = db.session.query(Listing)
    query.join(City, City.id == Listing.city_id)
    query.outerjoin(Manager, Manager.id == Listing.manager_id)
    query.outerjoin(Agent, Agent.id == Listing.agent_id)

    # Инициализация объекта DataTables и получение результатов для вывода
    row_table = DataTables(request.args, Listing, query, columns)
    result = row_table.output_result()

    # Форматирование дат в полях updated_at, created_at и добавление кнопок Show, Edit, Delete
    for x in result['data']:
        x['9'] = datetime.strptime(x['9'], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M:%S')
        x['10'] = datetime.strptime(x['10'], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M:%S')
        x['11'] = '''
            <a title="Show" href="{}" class="btn btn-primary"><i class="fa fa-eye"></i></a>
            <a title="Edit" href="{}" class="btn btn-warning"><i class="fa fa-edit"></i></a>
            <a title="Delete" href="{}" class="btn btn-danger delete"><i class="fa fa-remove"></i></a>
        '''.format(url_for('listings.show', listing_id=x['0']),
                   url_for('listings.edit', listing_id=x['0']),
                   url_for('listings.delete', listing_id=x['0']))

    # Возвращение результатов в формате JSON
    return jsonify(result)


@listings.route('/listings/street-addresses.json/<int:city_id>/')
def get_street_addresses(city_id):
    """Возвращает json с названиями улиц (поле *listings.street_address*) в городе *city_id*.
    Используется для автоподсказок в форме создания/редактирования листинга.

    :param city_id: Идентификатор города в таблице *cities*.
    :return: json
    """
    street_addresses = [m.street_address
                        for m in Listing.query
                        .with_entities(Listing.street_address)
                        .filter(Listing.city_id == city_id)
                        .order_by(Listing.street_address).all()
                        if m.street_address != '' and m.street_address is not None]
    return jsonify(street_addresses)


@listings.route('/listings/suburbs.json/<int:city_id>/')
def get_suburbs(city_id):
    """Возвращает json со значениями поля *listings.street_address* для города *city_id*.
    Используется для автоподсказок в форме создания/редактирования листинга.

    :param city_id: Идентификатор города в таблице *cities*.
    :return: json
    """
    suburbs = [m.suburb
               for m in Listing.query
               .with_entities(Listing.suburb)
               .filter(Listing.city_id == city_id)
               .order_by(Listing.suburb).all()
               if m.suburb != '' and m.suburb is not None]
    return jsonify(suburbs)
