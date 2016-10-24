from app import db
import datetime


class City(db.Model):
    """Класс модели для взаимодействия с таблицей БД *cities*."""
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime(),
                           default=datetime.datetime.now,
                           nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)

    def __init__(self, title):
        """ Конструктор класса.

        :param title: поле *title* в таблице.
        :type title: str
        """
        self.title = title


class Agent(db.Model):
    """Класс модели для взаимодействия с таблицей БД *agents*."""
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    agency = db.Column(db.String(255), default='')
    phone_numbers = db.Column(db.String(255), default='')
    email = db.Column(db.String(255), default='')
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    updated_at = db.Column(db.DateTime(),
                           default=datetime.datetime.now,
                           nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)

    city = db.relationship('City', backref=db.backref('agents', lazy='dynamic', cascade="all,delete"))

    def __init__(self, name, city_id, agency=None, phone_numbers=None, email=None):
        """ Конструктор класса.

        :param name: поле *name* в таблице.
        :type name: str
        :param city_id: поле *city_id* в таблице. Внешний ключ для *cities.id*.
        :type city_id: int
        :param agency: поле *agency* в таблице.
        :type agency: str
        :param phone_numbers: поле *phone_numbers* в таблице.
        :type phone_numbers: str
        :param email: поле *email* в таблице.
        :type email: str
        """
        self.name = name
        self.city_id = city_id
        self.agency = agency
        self.phone_numbers = phone_numbers
        self.email = email


class Manager(db.Model):
    """Класс модели для взаимодействия с таблицей БД *managers*."""
    __tablename__ = 'managers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    agency = db.Column(db.String(255), default='')
    phone_numbers = db.Column(db.String(255), default='')
    email = db.Column(db.String(255), default='')
    rate = db.Column(db.Float(), default=0, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    updated_at = db.Column(db.DateTime(),
                           default=datetime.datetime.now,
                           nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)

    city = db.relationship('City', backref=db.backref('managers', lazy='dynamic', cascade="all,delete"))

    def __init__(self, name, city_id, agency=None, phone_numbers=None, rate=0, email=None):
        """ Конструктор класса.

        :param name: поле *name* в таблице.
        :type name: str
        :param city_id: поле *city_id* в таблице. Внешний ключ для *cities.id*.
        :type city_id: int
        :param agency: поле *agency* в таблице.
        :type agency: str
        :param phone_numbers: поле *phone_numbers* в таблице.
        :type phone_numbers: str
        :param rate: поле *rate* в таблице.
        :type rate: float
        :param email: поле *email* в таблице.
        :type email: str
        """
        self.name = name
        self.city_id = city_id
        self.agency = agency
        self.phone_numbers = phone_numbers
        self.rate = rate
        self.email = email


class Listing(db.Model):
    """Класс модели для взаимодействия с таблицей БД *listings*."""
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.String(255), default='')
    street_address = db.Column(db.String(255), default='')
    suburb = db.Column(db.String(255), default='')
    property_type = db.Column(db.String(255), default='')
    bedrooms = db.Column(db.SmallInteger(), default=1)
    government_value = db.Column(db.Integer(), default=1)
    current_rates = db.Column(db.Integer(), default=1)
    median_rent_qv = db.Column(db.Integer(), default=1)
    capital_growth = db.Column(db.Float(), default=1)
    median_rent_tb = db.Column(db.Integer(), default=1)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    manager_id = db.Column(db.Integer,
                           db.ForeignKey('managers.id', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=True)
    updated_at = db.Column(db.DateTime(),
                           default=datetime.datetime.now,
                           nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)

    city = db.relationship('City', backref=db.backref('listings', lazy='dynamic', cascade="all,delete"))
    agent = db.relationship('Agent', backref=db.backref('listings', lazy='dynamic', cascade="all,delete"))
    manager = db.relationship('Manager', backref=db.backref('listings', lazy='dynamic', cascade="all,delete"))

    def __init__(self, city_id, street_number, street_address, suburb, property_type, bedrooms,
                 government_value=None, current_rates=None, median_rent_qv=None, capital_growth=None, median_rent_tb=None,
                 agent_id=None, manager_id=None):
        """Конструктор класса.

        :param city_id: поле *city_id* в таблице. Внешний ключ для `cities.id`.
        :type city_id: int
        :param street_number: поле *street_number* в таблице
        :type street_number: str
        :param street_address: поле *street_address* в таблице
        :type street_address: str
        :param suburb: поле *suburb* в таблице
        :type suburb: str
        :param property_type: поле *property_type* в таблице
        :type property_type: str
        :param bedrooms: поле *bedrooms* в таблице
        :type bedrooms: int
        :param government_value: поле *government_value* в таблице
        :type government_value: int
        :param current_rates: поле *current_rates* в таблице
        :type current_rates: int
        :param median_rent_qv: поле *median_rent_qv* в таблице
        :type median_rent_qv: int
        :param capital_growth: поле *capital_growth* в таблице
        :type capital_growth: float
        :param median_rent_tb: поле *median_rent_tb* в таблице
        :type median_rent_tb: int
        :param agent_id: поле *agent_id* в таблице. Внешний ключ для *agents.id*.
        :type agent_id: int
        :param manager_id: поле *manager_id* в таблице. Внешний ключ для *managers.id*.
        :type manager_id: int
        """
        self.city_id = city_id
        self.street_number = street_number
        self.street_address = street_address
        self.suburb = suburb
        self.property_type = property_type
        self.bedrooms = bedrooms
        self.government_value = government_value
        self.current_rates = current_rates
        self.median_rent_qv = median_rent_qv
        self.capital_growth = capital_growth
        self.median_rent_tb = median_rent_tb
        self.agent_id = agent_id
        self.manager_id = manager_id


