
# python

import lx, lifesaver


class StartupCommandClass(lifesaver.CommanderClass):

    def commander_execute(self, msg, flags):

        # In case user values have not been declared, declare them with default values
        # NOTE: we cannot declare these in configs because the list of KEEPERS is dynamic, not hard-coded.
        for i in lifesaver.KEEPERS:
            # We only declare a new user value if it doesn't already exist.
            if not lx.eval('query scriptsysservice userValue.isDefined ? %s' % i[3]):
                lx.eval('user.defNew %s boolean' % i[3])
                lx.eval('user.value %s true' % i[3])

        # We also need to declare this here instead of a config because otherwise it will be invalidated
        # on preferences reset.
        if not lx.eval('query scriptsysservice userValue.isDefined ? lifesaver_first_time_after_reset'):
            lx.eval('user.defNew lifesaver_first_time_after_reset boolean')
            lx.eval('user.value lifesaver_first_time_after_reset true')

        is_first_time = lx.eval("user.value lifesaver_first_time_after_reset ?")

        if is_first_time:
            try:
                lx.eval("lifesaver.mergePrefs")
            except:
                return lx.symbol.e_ABORT
            finally:
                lx.eval("user.value lifesaver_first_time_after_reset 0")
        else:
            mergeCmd = 'lifesaver.mergePrefs'
            for i in lifesaver.KEEPERS:
                mergeCmd += " " + str(lx.eval('lifesaver.preference %s ?' % i[3]))

            lx.eval(mergeCmd)

lx.bless(StartupCommandClass, 'lifesaver.startup')