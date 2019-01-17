from streaming_event_compliance import app, db
import time, traceback
from streaming_event_compliance.objects.logging.server_logging import ServerLogging
from streaming_event_compliance.objects.exceptions.exception import ThreadException, ReadFileException
from console_logging.console import Console
import sys


console = Console()
console.setVerbosity(5)


if __name__ == '__main__':
    func_name = sys._getframe().f_code.co_name
    try:
        ServerLogging().log_info(func_name, "Created all db tables")
        db.create_all()
    except Exception as ec:
        print('Error: Database connection!', ec.__class__, traceback.format_exc())
        ServerLogging().log_error(func_name, "Database connection error!")
        exit(1)

    from streaming_event_compliance.objects.variable.globalvar import gVars
    from streaming_event_compliance.services import setup
    from streaming_event_compliance.services.build_automata import build_automata
    from streaming_event_compliance.database import dbtools
    dbtools.empty_tables()  # TODO: After building the correct automata, uncomment this line;
    setup.init_automata()
    if gVars.auto_status == 0:
        start = time.clock()
        try:
            ServerLogging().log_info(func_name, "Building automata...")
            build_automata.build_automata()
        except ReadFileException as ec:
            print(ec.message)
            ServerLogging().log_error(func_name, "Training file cannot be read")
        except ThreadException as ec:
            print(ec.message)
            ServerLogging().log_error(func_name, "Error with threads")
        ends = time.clock()
        console.secure("[ The Total Time  ]", str(ends - start) + "Seconds.")

    else:
        print("Automata have been created in database and read out! You can use it do compliance checking!")
        ServerLogging().log_info(func_name, "Automata have been created in database and read out")
    # app.debug = False
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
