import lx, modo, life_server, datetime, os, sys, errno
from xml.etree import ElementTree

def get_this_kit_path():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    while len(this_dir) != 0 and not os.path.isfile(os.path.join(this_dir, "index.cfg")):
        this_dir = os.path.dirname(this_dir)
        
    return this_dir
    
def get_backup_config_path(tag_type):
    prefix = os.path.join(get_this_kit_path(), 'Configs', 'Backup')
    return "%s_%s.cfg" % (prefix, tag_type)
    
def get_modo_config_path():
    return lx.eval("query platformservice path.path ? configname")
    
def merge_unique_first(list1, list2, key):
    len1 = len(list1)
    len2 = len(list2)
    i,j = 0,0
    while (i < len1 and j < len2):
        if (key(list1[i]) < key(list2[j])):
            yield list1[i]
            i += 1
        elif (key(list1[i]) == key(list2[j])):
            # This case is not from true merge algorithm but will work in our case
            # Since we know that list1 and list2 are unique
            # Yielding first since the function name is merge_unique_first
            yield list1[i]
            i += 1
            j += 1
        else :
            yield list2[j]
            j += 1
            
    if (i == len1):
        while(j < len2):
            yield list2[j]
            j += 1
    elif (j == len2):
        while(i < len1):
            yield list1[i]
            i += 1
    
def merge_configs(modo_config_path, keepers):

    try:
        with open(modo_config_path, "r") as modo_config_file:
            modo_config_root = ElementTree.fromstring(unicode(modo_config_file.read(), errors='ignore'))
    except:
        modo.dialogs.alert("Failed", "Could not open config file.")
        return lx.symbol.e_FAILED

    kids = modo_config_root.getchildren()
    
    keeper_to_kids = dict()
    for keeper in keepers:
        keeper_to_kids[keeper] = list()

    for kid in kids:
        tag_type = kid.attrib.get("type", None)

        if tag_type in keepers:
            vals = kid.getchildren()
            vals.sort(key=lambda x: x.attrib.get("key", None))

            backup_config_path = get_backup_config_path(tag_type)
            try:
                with open(backup_config_path, "r") as backup_config_file:
                    backup_config_root = ElementTree.fromstring(unicode(backup_config_file.read(), errors='ignore'))
                backup_kids = backup_config_root.getchildren()
                if len(backup_kids) != 1 or backup_kids[0].attrib.get("type", None) != tag_type:
                    modo.dialogs.alert("Failed", "Corrupted backup file.")
                    return
                backup_vals = backup_kids[0].getchildren()
            except IOError as e:
                if e.errno == errno.ENOENT:
                    backup_vals = []
                else:
                    raise
                
            backup_vals.sort(key=lambda x: x.attrib.get("key", None))
            
            new_vals = ElementTree.Element(kid.tag, kid.attrib)
                
            lx.out(new_vals.getchildren())
            
            for val in merge_unique_first(vals, backup_vals, key=lambda x: x.attrib.get("key", None)):
                new_vals.append(val)
            
            with open(backup_config_path, 'wb') as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write('\n<!-- backup by life_server on %s -->\n\n' % datetime.datetime.now().strftime("%d-%M-%y at %H:%M"))
                file.write("<configuration>\n\n  ")
                file.write(ElementTree.tostring(new_vals))
                file.write("\n</configuration>")

class StartupCommandClass(life_server.CommanderClass):

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
      
        keepers = list()
        if self.commander_arg_value(0):
            keepers.append("InputRemapping")
        if self.commander_arg_value(1):
            keepers.append("DirBrowser")
        if self.commander_arg_value(2):
            keepers.append("Preferences")
        if self.commander_arg_value(3):
            keepers.append("AppGlobal")
    
        modo_config_path = get_modo_config_path()
        
        merge_configs(modo_config_path, keepers)
        
lx.bless(StartupCommandClass, 'life_server.startup')