@echo off
start /min cmd /c "C:&&cd %cd%\&&python manage.py  runserver 0.0.0.0:9000 --noreload"

