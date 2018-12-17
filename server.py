
from streaming_event_compliance import app, db
import time
from streaming_event_compliance.objects.exceptions.exception import ThreadException, ReadFileException

if __name__ == '__main__':

    try:
        db.create_all()
    except Exception as ec:
        print('Error: Database connection!', ec.__class__)
        exit(1)

    from streaming_event_compliance.services import globalvar
    from streaming_event_compliance.database import dbtools
    dbtools.empty_tables()  # TODO: After building the correct automata, uncommend this line;
    globalvar.init()
    auto_status = globalvar.get_autos_status()
    if auto_status == 0:
        start = time.clock()

        try:
            globalvar.call_buildautos()
        except ReadFileException as ec:
            print(ec.get_message())
        except ThreadException as ec:
            print(ec.get_message())

        ends = time.clock()
        print(ends - start)
    else:
        print("Automata have been created in database and readed out! You can use it do compliance checking!")
    app.debug = False
    app.run()
