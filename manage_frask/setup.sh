source ../data/bin/activate
FLASK_APP=run.py flask db init
FLASK_APP=run.py flask db migrate
FLASK_APP=run.py flask db upgrade