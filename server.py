
from streaming_event_compliance import app, db


if __name__ == '__main__':

    try:
        db.create_all()
    except Exception:
        print('Error: Database connection!')
        exit(1)

    from streaming_event_compliance.services import globalvar
    from streaming_event_compliance.database import dbtools
    dbtools.empty_tables()  # TODO: After building the correct automata, uncommend this line;
    globalvar.init()
    status = globalvar.get_autos_status()
    if status == 0:
        globalvar.call_buildautos()
    else:
        print("Automata have been created in database and readed out! You can use it do compliance checking!")

    app.debug = False
    app.run()
