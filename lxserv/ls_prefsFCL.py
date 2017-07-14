# python

import lx, lifesaver

def build_FCL():
    fcl = []
    for i in lifesaver.KEEPERS:
        fcl.append('lifesaver.preference %s ?' % i[3])
    return fcl

class CommandClass(lifesaver.CommanderClass):

    def commander_arguments(self):
        return [
                {
                    'name': 'query',
                    'datatype': 'integer',
                    'default': '',
                    'values_list_type': 'fcl',
                    'values_list': build_FCL,
                    'flags': ['query'],
                }
            ]

lx.bless(CommandClass, 'lifesaver.prefsFCL')