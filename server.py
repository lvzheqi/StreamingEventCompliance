from streaming_event_compliance import app, db
import time
from streaming_event_compliance.objects.exceptions.exception import ThreadException, ReadFileException
from console_logging.console import Console
console = Console()
console.setVerbosity(5)


if __name__ == '__main__':

    try:
        db.create_all()
    except Exception as ec:
        print('Error: Database connection!', ec.__class__)
        exit(1)

    from streaming_event_compliance.objects.variable.globalvar import gVars
    from streaming_event_compliance.services import setup
    from streaming_event_compliance.services.build_automata import build_automata
    from streaming_event_compliance.database import dbtools
    dbtools.empty_tables()  # TODO: After building the correct automata, uncommend this line;
    setup.init_automata()
    if gVars.auto_status == 0:
        start = time.clock()
        try:
            build_automata.build_automata()
        except ReadFileException as ec:
            print(ec.get_message())
        except ThreadException as ec:
            print(ec.get_message())
        ends = time.clock()
        console.secure("The Total Time:", str(ends - start) + "Seconds.")

    else:
        print("Automata have been created in database and readed out! You can use it do compliance checking!")
    app.debug = False
    app.run()
