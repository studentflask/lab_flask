Чтобы запустить приложение
1. Необходимо установить все пакеты из файлы requirements.txt
2. Из папки проекта запустить Gunicorn
gunicorn --bind 127.0.0.1:5000 wsgi:app --chdir flaskapp
