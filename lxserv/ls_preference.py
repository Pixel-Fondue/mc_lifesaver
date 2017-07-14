
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
                    'label': self.labler,
                    'datatype': 'string',
                    'default': "",
                    'flags': ['variable', 'query'],
                }
            ]

    def labler(self):
        for i in lifesaver.KEEPERS:
            if self.commander_arg_value(0) == i[3]:
                return i[1]

        return "[Error]"

    def commander_execute(self, msg, flags):
        name = self.commander_arg_value(0)
        value = self.commander_arg_value(1)
        pref = None
        pref_index = None

        for n, i in enumerate(lifesaver.KEEPERS):
            if name == i[3]:
                pref = i
                pref_index = n
                break

        if pref is not None:
            oldVal = bool(lx.eval("user.value %s ?" % pref[3]))

            if oldVal and not value and os.path.isfile(lifesaver.get_backup_config_path(pref[0])):
                msg = "This will delete %s backup data. Are you sure?" % pref[1]
                if modo.dialogs.yesNo("Are you sure?", msg) == 'no':
                    return

                clearCmd = "lifesaver.clearPrefs "

                for idx in xrange(0, len(lifesaver.KEEPERS)):
                    if idx == pref_index:
                        clearCmd += " 1"
                    else:
                        clearCmd += " 0"
                lx.eval(clearCmd)

            lx.eval("user.value %s %s" % (pref[3], value))

        if pref is None:
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
        return lx.symbol.sTYPE_BOOLEAN

#    def commander_notifiers(self):
#        return [("lifesaver.notifier", "")]

lx.bless(PreferenceCommandClass, "lifesaver.preference")
