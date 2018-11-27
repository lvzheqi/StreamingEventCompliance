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


from streaming_event_compliance import routes


from streaming_event_compliance.services import globalvar, set_globalvar, build_automata
from streaming_event_compliance.utils import dbtools


dbtools.empty_tables()

print(globalvar.autos, 'init之前')
print(set_globalvar.get_autos(), 'init之前get')
globalvar.init()
print(globalvar.autos, 'init之后')
print(set_globalvar.get_autos(), 'init之后get')
if set_globalvar.get_autos() is None:
    set_globalvar.call_buildautos()
else:
    print("Automata have beed created in database and readed out! You can use it do compliance checking!")

