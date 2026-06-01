@echo off
cd /d C:\controlgates

REM Ativar ambiente virtual
call venv\Scripts\activate

REM Rodar servidor
python manage.py runserver 0.0.0.0:8000

pause