from streaming_event_compliance import app, db
import time, traceback
from streaming_event_compliance.objects.logging.server_logging import ServerLogging
from streaming_event_compliance.objects.exceptions.exception import ThreadException, ReadFileException
from console_logging.console import Console
import sys, resource
resource.setrlimit(resource.RLIMIT_NOFILE, (2000, -1))
console = Console()
console.setVerbosity(5)

if __name__ == '__main__':
    func_name = sys._getframe().f_code.co_name
    try:
        ServerLogging().log_info(func_name, "Created all db tables")
        db.create_all()
    except Exception as ec:
        console.error('Error: Database connection!' + str(ec.__class__) + traceback.format_exc())
        ServerLogging().log_error(func_name, "Database connection error!")
        exit(1)

    from streaming_event_compliance.objects.variable.globalvar import gVars
    from streaming_event_compliance.services import setup
    from streaming_event_compliance.services.build_automata import build_automata
    from streaming_event_compliance.database import dbtools

    dbtools.empty_tables()
    setup.init_automata()
    if gVars.auto_status == 0:
        start = time.clock()
        console.secure("Start time: ", start)
        try:
            ServerLogging().log_info(func_name, "Building automata...")
            build_automata.build_automata()
        except ReadFileException as ec:
            console.error(ec.message)
            ServerLogging().log_error(func_name, "Training file cannot be read")
        except ThreadException as ec:
            ServerLogging().log_error(func_name, "Error with threads")
        except Exception as ec:
            ServerLogging().log_error(func_name, "Error")
        ends = time.clock()
        console.secure("[ The Total Time  For Training Automata  ]", str(ends - start) + "Seconds.")
    else:
        console.info("Automata have been created in database and read out! You can use it do compliance checking!")
        ServerLogging().log_info(func_name, "Automata have been created in database and read out")

    app.debug = False
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False, threaded=True)
