from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from streaming_event_compliance import config
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = config.BASE_DIR
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_PATH

db = SQLAlchemy(app)



from streaming_event_compliance import routes
