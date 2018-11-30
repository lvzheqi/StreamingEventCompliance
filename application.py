
from streaming_event_compliance import app, db
import time, os


def init_automata():
    from streaming_event_compliance.services import globalvar, set_globalvar
    from streaming_event_compliance.utils import dbtools

    db.create_all()
    dbtools.empty_tables()
    print(globalvar.autos, 'init之前')
    print(set_globalvar.get_autos(), 'init之前get')
    globalvar.init()
    # print(globalvar.autos, 'init之后')
    print(set_globalvar.get_autos(), 'init之后get')
    autos, status = set_globalvar.get_autos()
    if status == 0:
        set_globalvar.call_buildautos()
    else:
        print("Automata have beed created in database and readed out! You can use it do compliance checking!")



if __name__ == '__main__':
    print(os.getpid(), ' ', os.getppid())
    init_automata()
    # app.debug = True
    app.run()




