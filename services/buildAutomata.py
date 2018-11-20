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
    If the automata is not built, then will call the build_automata function to build the automata.
    And the status will be stored in config file.

    :return: status of the automata, or raise the exceptions when the automata can't be built.
    '''

    # TODO: create file to store the automata status
    # TODO: read file and assign to the globalVariables.AUTOMATA_STATUS
    if globalVariables.AUTOMATA_STATUS:
        return True
    else:
        # TODO: raise exceptions, when not success
        if (build_automata()):
            globalVariables.AUTOMATA_STATUS = True
            # TODO: rewrite to status into the file
