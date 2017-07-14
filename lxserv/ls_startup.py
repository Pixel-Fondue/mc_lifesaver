
# python

import lx, lifesaver

class StartupCommandClass(lifesaver.CommanderClass):

    def commander_arguments(self):
        return []

    def commander_execute(self, msg, flags):
        firstTime = lx.eval("lifesaver.preference lifesaver_first_time_after_reset ?")
        
        if firstTime:
            try:
                lx.eval("lifesaver.mergePrefs")
            except:
                return lx.symbol.e_ABORT
            finally:
                lx.eval("lifesaver.preference lifesaver_first_time_after_reset 0")
        else:
            mergeCmd = 'lifesaver.mergePrefs'
            for i in lifesaver.KEEPERS:
                mergeCmd += " " + str(lx.eval('lifesaver.preference %s ?' % i[3]))
        
            lx.eval(mergeCmd)
        
lx.bless(StartupCommandClass, 'lifesaver.startup')