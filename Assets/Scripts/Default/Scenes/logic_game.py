#icon=OUTLINER_DATA_CAMERA
import bge
import Background
from GamepadManager import Gamepad
from KeyboardManager import Keyboard
from collections import OrderedDict

class Game(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ])

    def start(self, args):
        self.gpad = Gamepad()
        self.keyb = Keyboard()
        pass
    
    def pause(self):
        if self.gpad.released('Start') or self.keyb.activated('esc'):
            bge.logic.addScene('Pause', True)
            self.object.scene.suspend()
            return
        
    def update(self):
        self.pause()
        pass
                
