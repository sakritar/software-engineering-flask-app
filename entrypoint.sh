## Проверяем, существует ли БД
#if [ ! -f /app/data/app.db ]; then
#  echo 'Initializing database...'
#  alembic upgrade head
#fi

alembic upgrade head
flask run --host=0.0.0.0 --port=8000
