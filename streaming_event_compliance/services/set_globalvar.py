from streaming_event_compliance.services.build_automata import build_automata
from streaming_event_compliance.services import globalvar

def change_autos(key,value):
    globalvar.autos[key] = value


def get_autos():
    return globalvar.autos, globalvar.status


def call_buildautos():
    build_automata.build_automata()


