
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
            backup_input_remapping = lx.eval("lifesaver.preference lifesaver_backup_input_remapping ?")
            backup_dir_browser = lx.eval("lifesaver.preference lifesaver_backup_preset_browser_state ?")
            backup_preferences = lx.eval("lifesaver.preference lifesaver_backup_preferences ?")
            backup_app_global = lx.eval("lifesaver.preference lifesaver_backup_global_settings ?")
            lx.eval("lifesaver.mergePrefs %s %s %s %s" % (backup_input_remapping, backup_dir_browser, backup_preferences, backup_app_global))
        
lx.bless(StartupCommandClass, 'lifesaver.startup')