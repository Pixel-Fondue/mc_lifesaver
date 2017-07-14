
# python

import lx, lifesaver, os

class ResetPrefsCommandClass(lifesaver.CommanderClass):

    def commander_execute(self, msg, flags):
        clearCmd = 'lifesaver.clearPrefs'
        for i in lifesaver.KEEPERS:
            clearCmd.append(str(lx.eval('lifesaver.preference %s ?' % i[0])))

        lx.eval(clearCmd)

lx.bless(ResetPrefsCommandClass, 'lifesaver.resetPrefs')