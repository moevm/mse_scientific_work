# IS_ScientificWork
ИС Кафедры: Научная работа

rootSite - основной каталог сайта (настройки и т.д.) <br>
scientificWork - приложение ИС "Научная работа"<br>
manage.py - системный файл Django для запуска/работы с сайтом

Для корректной работы необходимо изменить подключение к БД на ваше - в файле rootSite/settings.py 14 строка - DATABASES. После изменений необходимо выполнить команду "manage.py syncdb". Так же необходимо сверить SITE_ID(переменная в rootSite/settings.py) с тем, что будет указан в БД, в коллекции django_site.

Доступ к приложению: http://127.0.0.1:8000/scientificWork/
Административная панель: http://127.0.0.1:8000/admin/
