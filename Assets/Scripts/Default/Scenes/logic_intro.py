#icon=OUTLINER_DATA_CAMERA
import bge
from SettingsController import Settings
from collections import OrderedDict

class Intro(bge.types.KX_PythonComponent):
    """
    Component used for the intro scene (_Intro).
    Gets the screen default resolution and loads the  user settings; 
    Can be used to show initial credits (your logo, sponsorships etc...)
    """
    args = OrderedDict([
    ('next scene', "Menu"), 
    ('time target', 0), #seconds
    ])

    def start(self, args):
        # saves the resolution as the default
        bge.logic.loadGlobalDict()
        bge.logic.globalDict['monitor size'] = bge.render.getDisplayDimensions()
    
        # loads the user video settings and apply
        setting = Settings()
        setting._verify_global_dict()
        setting.apply()
        

        self.time = 0.0
        self.time_target = args['time target']
        self.next_scene = args['next scene']
        pass

    def update(self):
        # Goes to next when the timer is complete 
        self.time += 0.015
        self.object['time'] = self.time
        if self.time > self.time_target:
            self.object.scene.replace(self.next_scene)
        pass
