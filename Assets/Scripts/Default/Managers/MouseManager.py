#icon=SCRIPTWIN
import bge
from mathutils import Vector

class Mouse:
    def __init__(self, visible=True, set_center=False, sensi=1.0):
        """
        M
        """
        self.visible = visible
        self.mouse = bge.logic.mouse
        self.mouse.visible = self.visible
        self.last_pos = list(self.mouse.position)
        
        # mouse sensitiviy and screen
        self.sensitivity = sensi
        self.width = bge.render.getWindowWidth()
        self.height = bge.render.getWindowHeight()
        
        # Screen center tuple (Ideal to avoid argunment error)
        self.center = (0.5, 0.5)
        
        if set_center:
            self.mouse.position = self.center

    #================= Verify state method ==================

    def _get_input(self, key_code, state):
        """Process buttons state with error handling."""
        try:
            status = self.mouse.inputs.get(key_code)
            if status:
                if state == "active":     return status.active
                if state == "activated":  return status.activated
                if state == "released":   return status.released
            return False
        except Exception as e:
            print(f"[Mouse Error]: button failed {key_code}: {e}")
            return False

    #================= main mouse methods ==================
    
    def left_click(self):    return self._get_input(bge.events.LEFTMOUSE, "activated")
    def left_hold(self):     return self._get_input(bge.events.LEFTMOUSE, "active")
    def left_release(self):  return self._get_input(bge.events.LEFTMOUSE, "released")
    
    def right_click(self):   return self._get_input(bge.events.RIGHTMOUSE, "activated")
    def right_hold(self):    return self._get_input(bge.events.RIGHTMOUSE, "active")
    
    def middle_click(self):  return self._get_input(bge.events.MIDDLEMOUSE, "activated")
    def middle_hold(self):   return self._get_input(bge.events.MIDDLEMOUSE, "active")
    
    def click(self): return self.left_click()

    # --- SCROLL (RODA DO MOUSE) ---

    def scroll(self):
        """Return 1 to scroll up or -1 to scroll down else return 0"""
        try:
            up = self.mouse.inputs.get(bge.events.WHEELUPMOUSE)
            down = self.mouse.inputs.get(bge.events.WHEELDOWNMOUSE)
            
            if up and up.activated: return 1
            if down and down.activated: return -1
            return 0
        except:
            return 0

    # --- MOVEMENT (DELTA) ---

    def get_movement(self, reset=True):
        """Return a vector(x,y) with the mouse screen position
        :reset: Bool, move the mouse to screen center (ideal to FPS Gameplay)
        """
        try:
            current_pos = self.mouse.position

            x = self.center[0] - current_pos[0]
            y = self.center[1] - current_pos[1]
            
            delta = Vector([x, y]) * self.sensitivity
            
            if reset:
                self.mouse.position = self.center
                
            return delta
        except Exception as e:
            print(f"[Mouse Error]: Failed to calculate mouse movement: {e}")
            return Vector([0.0, 0.0])
    
    
    
    def on_movement(self, threshold=0.0):
        """
        Verify current mouse position.
        :return: diference new and between old mouse position 
        """
        current_pos = list(self.mouse.position)
        
        # Calcula a distância entre a posição atual e a do frame passado
        # Usamos Pitágoras simples: sqrt((x2-x1)^2 + (y2-y1)^2) (Importante notar que foi o chat GPT que fez :D)
        dx = current_pos[0] - self.last_pos[0]
        dy = current_pos[1] - self.last_pos[1]
        dist = (dx**2 + dy**2)**0.5
        
        self.last_pos = current_pos
        
        return dist > threshold
    
    
    def hover(self, distance=1000, prop=""):
        """
        Get the hovered mouse object
        :distance: target distance max
        :prop: object property target
        """
        try:
            scene = bge.logic.getCurrentScene()
            cam = scene.active_camera
            
            if not cam:
                print("[Mouse Warning]: Any camera active")
                return None
                
            mousePos = Vector(self.mouse.position)
            factor = 1920 / ((1080 / bge.render.getWindowHeight()) * bge.render.getWindowWidth())
            mousePos.y *= factor
            mousePos.y -= (factor - 1.0) / 2.0
            
            return cam.getScreenRay(mousePos[0], mousePos[1], distance, prop)
            
        except Exception as e:
            print(f"[Mouse Error]: Erro no Raycast (hover): {e}")
            return None
    