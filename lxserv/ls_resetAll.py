# python

import lx, modo, lifesaver

class ResetPrefsCommandClass(lifesaver.CommanderClass):

    def commander_execute(self, msg, flags):

        if modo.dialogs.yesNo("Confirm: Reset All Prefs", "All preferences AND backups will be deleted. This cannot be undone. Are you sure?") == "yes":

            clearCmd = 'lifesaver.clearPrefs'
            for i in lifesaver.KEEPERS:
                clearCmd += " " + str(lx.eval('lifesaver.preference %s ?' % i[3]))

            lx.eval(clearCmd)
            lx.eval('config.reset')

        else:
            modo.dialogs.alert("Abort", "Preferences reset aborted. Nothing will be deleted.")
            return


lx.bless(ResetPrefsCommandClass, 'lifesaver.resetAll')
