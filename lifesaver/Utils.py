# python

import os
import lx

def get_this_kit_path():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    while len(this_dir) != 0 and not os.path.isfile(os.path.join(this_dir, "index.cfg")):
        this_dir = os.path.dirname(this_dir)
        
    return this_dir

def get_user_config_path():    
    return lx.eval('query platformservice alias ? {Configs:}')
    
def get_backup_config_path(tag_type):
    prefix = os.path.join(get_user_config_path(), 'Backup')
    return "%s_%s.cfg" % (prefix, tag_type)
    
def get_modo_config_path():
    return lx.eval("query platformservice path.path ? configname")