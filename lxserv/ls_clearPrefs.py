#python

import lx, lifesaver, os

class ClearPrefsCommandClass(lifesaver.CommanderClass):

    def commander_arguments(self):
        return [
            {
                'name': 'inputRemapping',
                'datatype': 'boolean',
                'label': 'Backup Input Remapping',
                'default': True
            }, {
                'name': 'dirBrowser',
                'datatype': 'boolean',
                'label': 'Backup Preset Browser State',
                'default': True
            }, {
                'name': 'preferences',
                'datatype': 'boolean',
                'label': 'Backup Preferences',
                'default': True
            }, {
                'name': 'appGlobal',
                'datatype': 'boolean',
                'label': 'Backup Global Settings',
                'default': True
            }
        ]

    def commander_execute(self, msg, flags):
        backup_input_remapping = self.commander_arg_value(0)
        backup_dir_browser = self.commander_arg_value(1)
        backup_preferences = self.commander_arg_value(2)
        backup_app_global = self.commander_arg_value(3)
      
        to_clear = list()
        if backup_input_remapping:
            to_clear.append("InputRemapping")
        if backup_dir_browser:
            to_clear.append("DirBrowser")
        if backup_preferences:
            to_clear.append("Preferences")
        if backup_app_global:
            to_clear.append("AppGlobal")
    
        for type in to_clear:
            backup_config_path = lifesaver.get_backup_config_path(type)
            try:
                if os.path.isfile(backup_config_path):
                    os.remove(backup_config_path)
            except IOError as e:
                pass
                
lx.bless(ClearPrefsCommandClass, 'lifesaver.clearPrefs')