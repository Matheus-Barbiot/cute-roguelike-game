#icon=COLOR
import bge
from mathutils import Vector
from MouseManager import Mouse
from collections import OrderedDict
            
class Button(bge.types.KX_PythonComponent):
    """
    'Button' Component used to change the button color, when it is focused
    
    default color = (self.object.color) can be changed by 'object' menu from 'properties' menu on blender
    hover color = [R, G, B, A] defined in args from button.
    
    [IMPORTANT]
    The default use for this component is in the '_intro' scene, there is the object instance from button. 
    
    But you can create your own button, whether a group instance or a specific object
    
    """
    args = OrderedDict([
    ('hover color', [1,1,1,1]),
    ])

    def start(self, args):
        self.mouse = Mouse()
        self.hov_color = args['hover color']
        self.def_color = self.object.color.copy()
        
        if self.object.groupObject:
            self.object.visible = self.object.groupObject.visible
        
    def update(self):
        """ Change button color when it is focused """
        if not self.object.visible:
            return
        if self.object.scene.get("menu focus"):
            if self.object.groupObject == self.object.scene["menu focus"]:
                self.object.color = self.hov_color
            else:
                self.object.color = self.def_color
            
