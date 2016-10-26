***********
Инсталляция
***********

Данное руководство описывает установку приложения на сервер, но не настройку Web-сервера.
Поскольку в качестве Web-сервера можно использовать различное программное обеспечение, то подразумевается,
что настройка будет производится системным администратором. Руководства по настройке от разработчиков фреймворка **Flask**
можно посмотреть `тут <http://flask.pocoo.org/docs/0.11/deploying/>`_.

Если выбран вариант со связкой **nginx** + **uWSGI**, то следует учитывать, что файлы для конфигурации uwsgi
находятся в корне каталога проекта и называются *uwsgi.ini.example*, *project.service.example*.
Для работы их стоит переименовать на *uwsgi.ini*, *project.service* и отредактировать при необходимости.

Для установки **uWSGI** может необходима установка **python-devel**.

Установку условно можно разделить на несколько этапов:

Клонирование git-репозитория
----------------------------

Репозиторий проекта находится по адресу: `https://github.com/alexmon1989/houses_for_rents/ <https://github.com/alexmon1989/houses_for_rents/>`_.

Перейдите в каталог, где будет располагаться ваш проект, и выполните команду:

.. code-block:: bash

   git clone https://github.com/alexmon1989/houses_for_rents.git

Создание виртуального окружения Python
--------------------------------------

Перейдите к каталог проекта:

.. code-block:: bash

    cd house_for_rents

Установите пакет virtualenv:

.. code-block:: bash

    sudo pip3 install virtualenv

Создайте виртуальное окружение:

.. code-block:: bash

    virtualenv .env

Активируйте его:

.. code-block:: bash

    source .env/bin/activate

Установка Python библиотек
--------------------------

Установка библиотек для проекта производится командой:

.. code-block:: bash

    pip3 install -r requirements.txt

Настройка конфигурационного файла
---------------------------------

Переименуйте файл *config.py.example* в *config.py*.

Создание базы данных
--------------------

Испозьзуя любой доступный способ, создайте БД с параметрами:

| **Character set**: utf8 -- UTF-8 Unicode
| **Collation**: utf8_unicode_ci

БД можно создать следующим SQL-запросом:

.. code-block:: sql

    CREATE DATABASE IF NOT EXISTS `houses_for_rent` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;

Настройка подключения к MySQL
-----------------------------

В файле *config.py* найдите строку:

.. code-block:: python

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/houses_for_rent'

И замените:

| **user**: имя пользователя БД;
| **password**: пароль пользователя БД;
| **localhost**: IP-адрес БД;
| **houses_for_rent**: название БД.

После этого сохраните файл.

Применение миграций
-------------------

Для создания структуры БД необходимо воспользоваться механизмом миграций. Для этого выполните команду:

.. code-block:: bash

    python3 manage.py db upgrade

Наполнение базы данных начальными данными
-----------------------------------------

Для наполнения выполните команду:

.. code-block:: bash

    python3 seeder.py
