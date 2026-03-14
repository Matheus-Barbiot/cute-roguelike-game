#icon=SCRIPTWIN
import bge

class Settings():
    """
    'Settings' class with video configuration functions from bge.
    It is designed to be used together with the Settings component (logic_settings.py).
    """
    
    def __init__(self):
        self.resolutions_list = [(640, 480), (800, 600), (1280, 720), (1366, 768)]
        
        # Get the monitor screen size 
        try:
            self.monitor = bge.logic.globalDict.get('monitor size')
        except:
            print('[ERROR] The monitor screen size could not be detected')
            
        if not self.monitor in self.resolutions_list:
            self.resolutions_list.append(self.monitor)
        
        
        self.max_resolution_key = len(self.resolutions_list)-1
        
        #""" Default keys and values settings """
        self.default_settings = {
        'video': {
            'resolution key':  self.max_resolution_key, 
            'display mode': True, 
            'vsync mode': True,
            },
        'audio': {
            'general':  2.0,
            'music':    1.0, 
            'fx':   1.0,
            } 
        }
        
        
 
        
#=========================== video functions =========================
        
    def set_resolution(self, key):
        # Change game resolution
        size = self.resolutions_list[key] # ex: (600x800)
        bge.render.setWindowSize(*size) # y=600 x=800
        
        self._save_setting('resolution key', key)
        
    
    def set_display_mode(self, mode):
        # Change display mode (widescreen=False or fullscreen=True)
        bge.render.setWindowSize(*self.monitor)
        bge.render.setFullScreen(mode)
        
        self._save_setting('display mode', mode)
    
    
    def set_vsync_mode(self, mode):
        #Set the Vsync mode (0=False, 1=True)
        mode = int(mode)
        
        self._save_setting('vsync mode', mode)
        
    def apply(self):
        try:
            self.set_resolution(self._get_setting('resolution key'))
            self.set_display_mode(self._get_setting('display mode'))
            self.set_vsync_mode(self._get_setting('vsync mode'))
        except Exception as e:
            print(f'Erro ao APLICAR configurações: {e}')
      
#============================================================================  

    def _verify_global_dict(self):
        #Checks if the global dict is properly organized..
        global_dict = bge.logic.globalDict.get('_settings')
        padrao = self.default_settings
        
        
        if isinstance(global_dict, dict):
            compare = set(global_dict.keys()) == set(padrao.keys())
            if compare:
                return True
            
        print('[WARNING] GlobalDict: "_settings" from user corrupted. Applying default configuration.')
        bge.logic.globalDict['_settings'] = self.default_settings
        return False
        
        
    def _save_setting(self, settkey, value):
        #Save a specific setting in the globalDict
        self._verify_global_dict()
        
        try:
            if self._get_setting(settkey) != value:
                bge.logic.globalDict['_settings']['video'][settkey] = value
        except Exception as e:
            print(f'[ERRO] failed save: [{settkey}] = {value}: \n{e}')
            
    def _get_setting(self, key):
        #Return a specific video setting from globalDict
        self._verify_global_dict()
        
        try:
            return bge.logic.globalDict['_settings']['video'][key]
        except Exception as e:
            print(f'[ERRO] failed get: [video] -> [{key}]: {e}')
        
        
        
        