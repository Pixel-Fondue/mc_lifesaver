# python

import lx, lifesaver

class ResetPrefsCommandClass(lifesaver.CommanderClass):

    def commander_arguments(self):
        return [
            {
                'name': 'inputRemapping',
                'datatype': 'boolean',
                'label': 'Delete Input Remapping',
                'default': False
            }, {
                'name': 'dirBrowser',
                'datatype': 'boolean',
                'label': 'Delete Preset Browser State',
                'default': False
            }, {
                'name': 'preferences',
                'datatype': 'boolean',
                'label': 'Delete Preferences',
                'default': False
            }, {
                'name': 'appGlobal',
                'datatype': 'boolean',
                'label': 'Delete Global Settings',
                'default': False
            }
        ]

    def commander_execute(self, msg, flags):
        backup_input_remapping = self.commander_arg_value(0)
        backup_dir_browser = self.commander_arg_value(1)
        backup_preferences = self.commander_arg_value(2)
        backup_app_global = self.commander_arg_value(3)

        if True not in [backup_input_remapping, backup_dir_browser, backup_preferences, backup_app_global]:
            modo.dialogs.alert("Abort", "Nothing was selected. Nothing will be deleted.")
            return

        if modo.dialogs.yesNo("Confirmation", "Are you sure you want to permanently delete your saved preferences?") == "yes":

            # Only ask for preferances that have backup
            clearCmd = "lifesaver.clearPrefs "
            clearCmd += str(lx.eval("lifesaver.preference lifesaver_backup_input_remapping ?")) + " "
            clearCmd += str(lx.eval("lifesaver.preference lifesaver_backup_preset_browser_state ?")) + " "
            clearCmd += str(lx.eval("lifesaver.preference lifesaver_backup_preferences ?")) + " "
            clearCmd += str(lx.eval("lifesaver.preference lifesaver_backup_global_settings ?")) + " "

            lx.eval(clearCmd)

            modo.dialogs.alert("Preferences Deleted", "The selected preferences have been deleted.")

        else:
            modo.dialogs.alert("Abort", "Preferences reset aborted. Nothing will be deleted.")
            return


lx.bless(ResetPrefsCommandClass, 'lifesaver.resetPrefsSafety')
