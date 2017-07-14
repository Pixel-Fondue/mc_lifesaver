# python

KEEPERS = [
# Format key,               ???,               ???,   ???,              , mergeOrCopy
         ['InputRemapping', 'Input Remapping', True, 'ls_inputRemapping', True],
         ['DirBrowser', 'Preset Browser Paths', True, 'ls_dirBrowser', True],
         ['Preferences', 'Preferences', True, 'ls_preferences', True],
         ['AppGlobal', 'Global Settings', True, 'ls_appGlobal', True],
         ['UserValues', 'User Values', True, 'ls_UserValues', True],
         ['HudCustomTools_Edit', 'HUD Customizations', True, 'ls_HudCustomTools_Edit', False],
         ['AttributeRecentsAndFrequents', 'Recent and Frequent Tools', True, 'ls_AttributeRecentsAndFrequents', False]
]

# TODO Make access function for all data
def mergeKeeper(key):
    for idx in xrange(0, len(KEEPERS)):
        if KEEPERS[idx][0] == key:
            return KEEPERS[idx][4]
    
    return None

