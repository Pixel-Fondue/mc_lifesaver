# python

import lx, modo, lifesaver

class ResetPrefsCommandClass(lifesaver.CommanderClass):

    def commander_arguments(self):
        args = []

        for i in lifesaver.KEEPERS:
            args.append({
                'name': i[0],
                'datatype': 'boolean',
                'label': i[1],
                'default': True
            })

        return args

    def commander_execute(self, msg, flags):
        args = self.commander_args()

        if True not in [v for k, v in args.iteritems()]:
            modo.dialogs.alert("Abort", "Nothing was selected. Nothing will be deleted.")
            return

        if modo.dialogs.yesNo("Confirmation", "Are you sure you want to permanently delete your saved preferences?") == "yes":

            clearCmd = 'lifesaver.clearPrefs'
            for i in lifesaver.KEEPERS:
                clearCmd += " " + str(lx.eval('lifesaver.preference %s ?' % i[3]))

            lx.eval(clearCmd)

            modo.dialogs.alert("Preferences Deleted", "Backup configs deleted. Changes take effect the next time MODO restarts.")

        else:
            modo.dialogs.alert("Abort", "Preferences reset aborted. Nothing will be deleted.")
            return


lx.bless(ResetPrefsCommandClass, 'lifesaver.resetPrefsSafety')
