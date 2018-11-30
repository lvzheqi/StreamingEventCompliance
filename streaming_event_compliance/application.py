
from streaming_event_compliance import app, db


if __name__ == '__main__':
    from streaming_event_compliance.services import globalvar, set_globalvar, build_automata
    from streaming_event_compliance.utils import dbtools

    try:
        db.create_all()
    except Exception:
        print('Error: Database connection!')
        exit(1)
    dbtools.empty_tables()
    print(globalvar.autos, 'init之前')
    print(set_globalvar.get_autos(), 'init之前get')
    globalvar.init()
    print(globalvar.autos, 'init之后')
    print(set_globalvar.get_autos(), 'init之后get')
    autos, status = set_globalvar.get_autos()
    if status == 0:
        set_globalvar.call_buildautos()
    else:
        print("Automata have beed created in database and readed out! You can use it do compliance checking!")

    app.debug = True
    app.run()




