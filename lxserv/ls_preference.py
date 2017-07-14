
# python

import lx, lxifc, modo, lifesaver, os

class PreferenceCommandClass(lifesaver.commander.CommanderClass):
    def commander_arguments(self):
        return [
                {
                    'name': 'name',
                    'datatype': 'string',
                    'flags': ['reqforvariable'],
                }, {
                    'name': 'value',
                    'datatype': 'string',
                    'default': "",
                    'flags': ['variable', 'query'],
                }
            ]
            
    _keepers_info = {"lifesaver_backup_input_remapping" : ("input remapping", 0, "InputRemapping"),
               "lifesaver_backup_preset_browser_state" : ("preset browser stat", 1, "DirBrowser"),
               "lifesaver_backup_preferences" : ("preferences", 2, "Preferences"),
               "lifesaver_backup_global_settings" : ("global settings", 3, "AppGlobal")}
               
    def keepers():
        def fget(self):
            return self.__class__._keepers_info.keys()
        return locals()

    keepers = property(**keepers())    
    
    def keeper_description(self, prefName):
        return self.__class__._keepers_info[prefName][0]
        
    def keeper_arg_pos(self, prefName):
        return self.__class__._keepers_info[prefName][1]
        
    def keeper_internal_name(self, prefName):
        return self.__class__._keepers_info[prefName][2]

    def commander_execute(self, msg, flags):
        value = self.commander_arg_value(1)
        name = self.commander_arg_value(0)

        if name in self.keepers:
            oldVal = bool(lx.eval("user.value %s ?" % name))
            if oldVal and not value and os.path.isfile(lifesaver.get_backup_config_path(self.keeper_internal_name(name))):
                msg = "This will delete back %s backup data. Are you sure?" % self.keeper_description(name)
                if modo.dialogs.yesNo("Are you sure?", msg) == 'no':
                    return
                clearCmd = "lifesaver.clearPrefs "
                for idx in xrange(0, len(self.keepers)):
                    if idx == self.keeper_arg_pos(name):
                        clearCmd += " 1"
                    else:
                        clearCmd += " 0"
                lx.eval(clearCmd)
            else:
                lx.eval("user.value %s %s" % (name, value))
        else:
            lx.eval("user.value %s %s" % (name, value))

        # notifier = lifesaver.Notifier()
        # notifier.Notify(lx.symbol.fCMDNOTIFY_CHANGE_ALL)
        
    def basic_Enable(self, msg):
        return True

    def cmd_Query(self, index, vaQuery):
        name = self.commander_arg_value(0)

        # Create the ValueArray object
        va = lx.object.ValueArray()
        va.set(vaQuery)

        va.AddInt(lx.eval("user.value %s ?" % name))
        
        return lx.result.OK
        
    def basic_ArgType(self, argIndex):
        return 'boolean'

#    def commander_notifiers(self):
#        return [("lifesaver.notifier", "")]

lx.bless(PreferenceCommandClass, "lifesaver.preference")
