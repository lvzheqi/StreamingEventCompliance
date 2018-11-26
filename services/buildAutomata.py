from utils import globalVariables


def build_automata():
    '''
    Reads the training event log from utils.config.TRAINING_EVENT_LOG and build automata.
    It generates the probability between SourceNode and SinkNode with different prefix size
    and stores corresponding information into the database.
    :return: the status of the automata
    '''
    # Instantiate an object Automata.
    # Connect to the database
    # Read file
    # Calculating
    # TODO: raise exception when not success

    return True


def test_automata_status():
    '''
    This function will check whether the automata is built. If the automata isn’t yet built,
    then will call the build_automata function to build the automata.
    And the status will be stored in “Compliance.config”.
    It raises the exceptions when the automata can not  be built.
    :return: status of the automata
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
