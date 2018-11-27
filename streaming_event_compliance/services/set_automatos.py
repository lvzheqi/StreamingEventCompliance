from streaming_event_compliance.services import globalvar
from streaming_event_compliance.services import build_automata


def change_autos(key,value):
    globalvar.autos['key'] = value
    # self.autos = dbtools.init_automata()
    # if Globalvar.autos is None:
    #     for ws in WINDOW_SIZE:
    #         auto = automata.Automata(ws)
    #         Globalvar.autos[ws] = auto
    #     build_automata.build_automata()
    # else:
    # print("2: 初始化的autos", globalvar.autos)
    # globalvar.autos['1'] = 'aaa'
    # print("3: 全局变量文件里应该传出去的", globalvar.autos)

def get_autos():
    return globalvar.autos

def call_build():
    if not get_autos():
        build_automata.build_automata()

