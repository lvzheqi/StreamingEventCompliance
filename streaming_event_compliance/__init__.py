from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from streaming_event_compliance import config

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = config.BASE_DIR
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_PATH


db = SQLAlchemy(app)
try:
    db.create_all()
except Exception:
    print('Error: Database connection!')
    exit(1)

print('__init__test')

from streaming_event_compliance import routes
