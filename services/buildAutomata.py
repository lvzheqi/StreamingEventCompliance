from config import globalVariables


def build_automata():
    '''
    This function will get the value of variable 'path' which indicates a event_log file
    from config.defaultConfig, use it to build automata and store corresponding
    information into the database.
    :return: boolean
    '''
    # Instantiate an object Automata.
    # Connect to the database
    # Read file
    # Calculating
    # TODO: raise exception when not success

    return True


def test_automata_status():
    '''
    This function will check whether the automate is built or not.
    :return:
    '''

    # TODO: create file to store the automata status
    # TODO: read file and assign to the globalVariables.AUTOMATA_STATUS
    if globalVariables.AUTOMATA_STATUS:
        return True
    else:
        # TODO: try catch exception, when not success more than 2 times
        while (build_automata()):
            globalVariables.AUTOMATA_STATUS = True
            # TODO: rewrite to status into the file
