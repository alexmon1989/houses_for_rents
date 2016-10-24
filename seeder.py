# coding: utf-8
from app import db
from app.models import City, Agent, Manager, Listing


def clear_db():
    """Очистка таблиц БД"""
    db.engine.execute("SET FOREIGN_KEY_CHECKS=1;")
    db.session.query(City).delete()
    db.session.query(Agent).delete()
    db.session.query(Manager).delete()
    db.session.query(Listing).delete()
    db.session.commit()
    db.engine.execute("ALTER TABLE `cities` AUTO_INCREMENT = 1;")
    db.engine.execute("ALTER TABLE `agents` AUTO_INCREMENT = 1;")
    db.engine.execute("ALTER TABLE `managers` AUTO_INCREMENT = 1;")
    db.engine.execute("ALTER TABLE `listings` AUTO_INCREMENT = 1;")
    db.engine.execute("SET FOREIGN_KEY_CHECKS=1;")


def seed_cities():
    """Заполнение таблицы `cities`"""
    moscow = City(title='Moscow')
    tula = City(title='Tula')
    db.session.add(moscow)
    db.session.add(tula)
    db.session.commit()


def seed_agents():
    """Заполнение таблицы `agents`"""
    ivanov = Agent(name='Ivanov Ivan', city_id=1)
    petrov = Agent(name='Petrov Petr', city_id=2)
    db.session.add(ivanov)
    db.session.add(petrov)
    db.session.commit()


def seed_managers():
    """Заполнение таблицы `managers`"""
    fedorov = Manager(name='Fedorov Fedor', city_id=1)
    alexandrov = Manager(name='Alexandrov Alexandr', city_id=2)
    db.session.add(fedorov)
    db.session.add(alexandrov)
    db.session.commit()


def seed_listings():
    """Заполнение таблицы `listings`"""
    l1 = Listing(street_address='Street Address 1',
                 street_number='Street Number 1',
                 city_id=1,
                 suburb='suburb 1',
                 bedrooms=2,
                 property_type='property type 1',
                 agent_id=1,
                 manager_id=1)
    l2 = Listing(street_address='Street Address 2',
                 street_number='Street Number 2',
                 suburb='suburb 2',
                 bedrooms=6,
                 property_type='property type 2',
                 city_id=2,
                 agent_id=2,
                 manager_id=2)
    db.session.add(l1)
    db.session.add(l2)
    db.session.commit()


if __name__ == "__main__":
    print('Очистка таблиц...')
    clear_db()
    print('Заполнение таблицы cities...')
    seed_cities()
    print('Заполнение таблицы agents...')
    seed_agents()
    print('Заполнение таблицы managers...')
    seed_managers()
    print('Заполнение таблицы listings...')
    seed_listings()
