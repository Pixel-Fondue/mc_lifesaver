
# python

import lx, lifesaver, os

class ResetPrefsCommandClass(lifesaver.CommanderClass):

    def commander_arguments(self):
        return []

    def commander_execute(self, msg, flags):
        
        # Only ask for preferances that have backup
        clearCmd = 'lifesaver.clearPrefs'
        for i in lifesaver.KEEPERS:
            clearCmd += " " + str(lx.eval('lifesaver.preference %s ?' % i[3]))
        
        lx.eval(clearCmd)
      
                
lx.bless(ResetPrefsCommandClass, 'lifesaver.resetPrefs')