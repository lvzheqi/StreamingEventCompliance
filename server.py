
from streaming_event_compliance import app, db


if __name__ == '__main__':

    try:
        db.create_all()
    except Exception:
        print('Error: Database connection!')
        exit(1)

    from streaming_event_compliance.services import set_globalvar, globalvar
    from streaming_event_compliance.database import dbtools
    dbtools.empty_tables()
    globalvar.init()
    autos, status = set_globalvar.get_autos()
    if status == 0:
        set_globalvar.call_buildautos()
    else:
        print("Automata have been created in database and readed out! You can use it do compliance checking!")

    app.debug = False
    app.run()
