
# python

import lx, lifesaver, os

class ResetPrefsCommandClass(lifesaver.CommanderClass):

    def commander_arguments(self):
        return []

    def commander_execute(self, msg, flags):
        
        # Only ask for preferances that have backup
        clearCmd = "lifesaver.clearPrefs "
        clearCmd += str(lx.eval("lifesaver.preference lifesaver_backup_input_remapping ?")) + " "
        clearCmd += str(lx.eval("lifesaver.preference lifesaver_backup_preset_browser_state ?")) + " "
        clearCmd += str(lx.eval("lifesaver.preference lifesaver_backup_preferences ?")) + " "
        clearCmd += str(lx.eval("lifesaver.preference lifesaver_backup_global_settings ?")) + " "
        
        lx.eval(clearCmd)
      
                
lx.bless(ResetPrefsCommandClass, 'lifesaver.resetPrefs')