
# python

import lx, lifesaver

class StartupCommandClass(lifesaver.CommanderClass):

    def commander_execute(self, msg, flags):

        # In case user values have not been declared, declare them with default values
        for i in lifesaver.KEEPERS:
            if not lx.eval('query scriptsysservice userValue.isDefined ? %s' % i[3]):
                lx.eval('user.defNew %s boolean' % i[3])
                lx.eval('user.value %s true' % i[3])

        firstTime = lx.eval("lifesaver.preference lifesaver_first_time_after_reset ?")
        
        if firstTime:
            try:
                lx.eval("lifesaver.mergePrefs")

            except:
                return lx.symbol.e_ABORT

            finally:
                lx.eval("lifesaver.preference lifesaver_first_time_after_reset 0")

        else:
            cmd = 'lifesaver.mergePrefs'
            for i in lifesaver.KEEPERS:
                pref = lx.eval('lifesaver.preference %s ?' % i[3])
                cmd += " %s" % pref
            lx.eval(cmd)
        
lx.bless(StartupCommandClass, 'lifesaver.startup')