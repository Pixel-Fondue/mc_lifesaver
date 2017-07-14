# python

import lx, lifesaver

def build_FCL():
    fcl = []
    for i in lifesaver.KEEPERS:
        fcl.append('lifesaver.preference %s ?' % i[3])
    return fcl

class ResetPrefsCommandClass(lifesaver.CommanderClass):

    def commander_arguments(self):
        return [{
                'name': 'query',
                'values_list': build_FCL,
                'values_list_type': 'FCL',
                'flags': ['query']
            }]

lx.bless(ResetPrefsCommandClass, 'lifesaver.prefsFCL')