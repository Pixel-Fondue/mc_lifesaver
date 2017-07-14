#python

import lx, lifesaver, os

class ClearPrefsCommandClass(lifesaver.CommanderClass):

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

        keepers = [key for key, enabled in args.iteritems() if enabled]
        for key in keepers:

            backup_config_path = lifesaver.get_backup_config_path(key)

            try:
                if os.path.isfile(backup_config_path):
                    os.remove(backup_config_path)

            except IOError as e:
                pass
                
lx.bless(ClearPrefsCommandClass, 'lifesaver.clearPrefs')