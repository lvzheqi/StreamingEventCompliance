from flask import Flask
from streaming_event_compliance.utils import config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = config.BASE_DIR
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_PATH


db = SQLAlchemy(app)
try:
    db.create_all()
except Exception:
    print('Error: Database connection!')
    exit(1)

from streaming_event_compliance.services.build_automata.build_automata import init_automata
autos = init_automata()

from streaming_event_compliance import routes
