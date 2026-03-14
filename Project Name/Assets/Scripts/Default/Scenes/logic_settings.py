#icon=OUTLINER_DATA_CAMERA
import bge
from SettingsController import  Settings as Set
from collections import OrderedDict
from MouseManager import Mouse


class Settings(bge.types.KX_PythonComponent):
    """ 
    'Settings' component to use in the 'Settings' scene.
    Can change the resolution, screen mode(window or fullscren) and active Vsync
    
    [IMPORTANT]
    This component is not highly flexible. 
    It operates in parallel with:
        
        - VisualSettings component (visualSettingsController.py)
            Responsible for update in real time the user settings
    
        - Menu component (logic_menu.py)
            Responsible for the menu navigation 
            
        - Settings 
            Responsible for the video functions
        
        - Clear GlobalDict
            any fail on globalDict structure can break the system
    
    So if you change this code, delete or add a option, make sure it doesn't conflict.
    
    
    """
    args = OrderedDict([
    ])
    
    def start(self, args):
        self.setting = Set()
        self.mouse = Mouse(True)
        
        self.set_funcs = {
            'resolution': self.set_screen_size,
            'display': self.set_display_mode,
            'vsync': self.set_vsync,
            'volume': self.set_volume,
        }
        
        self.gd_funcs = {
            'save': self.save_settings,
            'cancel': self.cancel_settings,
            'reset': self.reset_settings
        }
        


#===================================
    # Video configuration functions
#===================================

    def set_screen_size(self, num):
        max = self.setting.max_resolution_key
        func = self.setting.set_resolution
        
        value = self.__to_int_func('resolution key', 'video', num, max, func)
        self.object['set visual'] = 'screen'
        return value
        
        
    def set_display_mode(self, mode):
        value = self.__to_bool_func('display mode', mode, self.setting.set_display_mode)
        self.object['set visual'] = 'display'
        return value


    def set_vsync(self, mode):
        value = self.__to_bool_func('vsync mode', mode, self.setting.set_vsync_mode)
        self.object['set visual'] = 'vsync'
        return value
    
        
    def set_volume(self, key, num):        
        value = self.__to_int_func(key, 'audio', num, max=2)
        self.object['set visual'] = 'volume'
        
        return(value)
    
#====================================================
#       GlobalDict Functions
#====================================================

    def reset_settings(self):
        """ revert to settings from globalDict and set the default """
        bge.logic.globalDict['_settings'] = self.setting.default_settings
        self.setting.apply()
        
        self.object['set visual'] = 'all'
        print('algo')
        
    def cancel_settings(self):
        """ Cancel the settings, back to settings in the globalDict """
        bge.logic.loadGlobalDict()
        self.setting.apply()
        
        self.object['set visual'] = 'all'
    
    def save_settings(self):
        bge.logic.saveGlobalDict()
        
#====================================================

    def update(self):
        hovered = self.mouse.hover()
        
        if self.mouse.click() and hovered:
            button = hovered.groupObject if hovered.groupObject else hovered
            if 'setting' in button:
                if button['setting'] == 'gd':
                    print(button.name)
                    for key, func in self.gd_funcs.items():
                        if key in button:
                            func()
                            print(key, button.name)
                
                elif button['setting'] == 'set':
                    
                    for key, func in self.set_funcs.items():
                        if key in button:
                            
                            if key == 'volume':
                                value = func(button['type'], button[key])
                                self.object[button['type']] = value
                            else:
                                value = func(button[key])
                                print(key, button.name)
                                self.object[key] = value
                                
                            if isinstance(button[key], bool):
                                button[key] = value

#################################################
# Funções privadas
#################################################

    def __to_bool_func(self, key, mode, func):
        """ Ideal for Vsync e Screen mode. Get and verifies input boolean values. """
        current_mode = bge.logic.globalDict['_settings']['video'][key]
        
        new_mode = not mode
        if current_mode == new_mode:
            return new_mode
        
        func(new_mode)
        bge.logic.globalDict['_settings']['video'][key] = new_mode
        return new_mode
    
    
    
    def __to_int_func(self, key, category, num, max, func=None):
        """ Get and verifies input int values """
        current = bge.logic.globalDict['_settings'][category][key]
        
        new = current + num
        
        if new > max or new < 0.0:
            return current
        
        if func:
            func(new)
        bge.logic.globalDict['_settings'][category][key] = new
        return new