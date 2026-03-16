#icon=MESH_CUBE
import bge
from mathutils import Vector
from collections import OrderedDict
from GamepadManager import Gamepad
from KeyboardManager import Keyboard
from MouseManager import Mouse

class Player(bge.types.KX_PythonComponent):
    """
    Initial player component, a test drive for the gamepad, keyboard and mouse functions:
    """
    args = OrderedDict([
        ('speed', 0.15)
    ])

    def start(self, args):
        self.character = bge.constraints.getCharacter(self.object)
        self.keyboard = Keyboard()
        self.gamepad = Gamepad()
        self.mouse = Mouse(visible=False)
        
        self.speed = args['speed']
        pass

    def movement(self):
        Y = self.keyboard.value("W") - self.keyboard.value("S") or self.gamepad.get_axis("left", "Y")
        X = self.keyboard.value("D") - self.keyboard.value("A") or self.gamepad.get_axis("left", "X")
            
            
        if self.keyboard.active('space') or self.gamepad.pressed("A"):
            self.character.jump() 
        
        direction = self.object.worldOrientation * Vector([X, Y, 0])
        self.character.walkDirection =  direction.normalized() * self.speed
        
        
    def cam_lock(self):
        X = self.mouse.get_movement(reset=True)[0] or self.gamepad.get_axis('right', 'X') * -0.1
            
        self.object.applyRotation([0,0,X], True)
        
        
    def update(self):
        self.movement()
        self.cam_lock()
        pass

