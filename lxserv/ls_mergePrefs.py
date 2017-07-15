
# python

import lx, modo, lifesaver, datetime, errno
from xml.etree import ElementTree
    
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
        # This could happen after reset preference. Everything is OK continue.
        return

    kids = modo_config_root.getchildren()
    
    for kid in kids:
        tag_type = kid.attrib.get("type", None)

        if tag_type in keepers:
            vals = kid.getchildren()
            vals.sort(key=lambda x: x.attrib.get("key", None))

            backup_config_path = lifesaver.get_backup_config_path(tag_type)
            new_vals = ElementTree.Element(kid.tag, kid.attrib)
            if lifesaver.merge_keeper(tag_type):
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
            
                for val in merge_unique_first(vals, backup_vals, key=lambda x: x.attrib.get("key", None)):
                    new_vals.append(val)
            else:
                new_vals = vals
            
            with open(backup_config_path, 'wb') as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write('\n<!-- backup by lifesaver on %s -->\n\n' % datetime.datetime.now().strftime("%d-%M-%y at %H:%M"))
                file.write("<configuration>\n\n  ")
                for i in new_vals:
                    file.write(ElementTree.tostring(i))
                file.write("\n</configuration>")

class MergePrefsCommandClass(lifesaver.CommanderClass):

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

        modo_config_path = lifesaver.get_modo_config_path()

        keepers = [key for key, enabled in args.iteritems() if enabled]
        merge_configs(modo_config_path, keepers)

        for k, v in args.iteritems():
            for i in lifesaver.KEEPERS:
                if i[0] == k:
                    lx.eval("lifesaver.preference %s %s" % (i[3], v))
                break

lx.bless(MergePrefsCommandClass, 'lifesaver.mergePrefs')