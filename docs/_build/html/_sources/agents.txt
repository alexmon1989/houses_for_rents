*************
Модуль Agents
*************

Модель
======

Основной моделью модуля является :ref:`agent-model`.

Контроллер
==========

Исходный код контроллера модуля расположен в файле *app/blueprints/agents/views.py*.


Методы контроллера:

.. automodule:: app.blueprints.agents.views
	:members:


Шаблоны
=======

Шаблоны модуля расположены в каталоге *app/templates/agents*

Формы
=====

Форма для добавления и редактирования листинга описывается классом **AgentForm** в файле *app/blueprints/agents/forms.py*.
Этот класс отвечает также за валидацию введённых пользователем данных.

.. automodule:: app.blueprints.agents.forms
	:members: