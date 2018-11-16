from config import globalVariables


def build_automata():
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
