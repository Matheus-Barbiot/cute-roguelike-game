#icon=OUTLINER_DATA_CAMERA
import bge
from collections import OrderedDict
from MouseManager import Mouse
from KeyboardManager import Keyboard
from GamepadManager import Gamepad
from MenuController import MenuController

class Menu(bge.types.KX_PythonComponent):
    """
    "Menu" is a base component shared by all menu scenes. 
    Add to the scene's active camera from menu scene.
    
    [Grid]
        Menu scenes are configured with an imaginary grid. 
        Buttons(rows) is parented to empty objects(columns). 
        
        [why?]
        the grid will define the focus navigation if using joystick dpad or keyboard arrows to navegate.
    
    [Button] 
        on 3D viewport press SHIFT+A and add the group instance "UI_Button". This is a functional button.
        
    [important] 
        column -> ALWAYS parent a button on a Empty object, in this empty object add the "column" property.
        
        command -> if your button triggers a specifc menu command (ex: "start", "back", "restart", etc...) 
            add the "command" property with the command value (any key name from the self.commands_dict)
        
        set_scene -> if your button accesses a specific scene, add "set scene" property with the specific scene name.
    """
    
    args = OrderedDict([
        ('game scene', 'Game'),
        ('main menu', 'Menu'),
        ('previous scene', ''),
    ])
    
    def start(self, args): 
        self.mouse = Mouse(visible=True)
        self.keyboard = Keyboard()
        self.gamepad = Gamepad()
        self.button_focus = None
        
        self.home = args['main menu']
        self.game = args['game scene']
        
        # Get the previousily defined scene or fall back to the global dict
        if args['previous scene'] == '':
            self.previous = bge.logic.globalDict.get('previous menu')
        else:
            self.previous = args['previous scene'] 
            
        self.menu = MenuController(self.home, self.previous)
        
        # GRID CONFIGURED (2 steps)
        
        # [STEṔ 1] list the columns from the grid, ordered by 'world position X' each object
            # IMPORTANT -> to be recognized, the empty object must have "column" property
        self.columns = sorted(
            [c for c in self.object.scene.objects if "column" in c], 
            key=lambda obj: obj.worldPosition.x
        )

        #  [STEP 2] list all child of columns, forming the grid,
        # ordered by 'world position Y' each object.

        self.grid = [
            sorted([r for r in c.children], key=lambda r: -r.worldPosition.y) 
            for c in self.columns
        ]

        # define the initial focus 
        self.focus = [0, 0] # column, button keys
        self.mouse_active = False

        # get the object focus using the keys
        if self.grid and self.grid[0]:
            self.button_focus = self.grid[self.focus[0]][self.focus[1]]
            #print(f"Initial focus: {self.button_focus.name}")
            
            self.object.scene["menu focus"] = self.button_focus
        
        
        # Generic menu functions
        self.commands_dict = {
            'play'    : self.play,
            'restart' : self.play,
            'quit'    : self.quit,
            'resume'  : self.resume,
            'back'    : self.menu.back,
            'home'    : self.menu.return_home,
        }
        
        # Define the current scene as the 'previous scene' from global dict.
        # this allow the 'back' function to back this scene.
        self._update_previous()
        
    
    def _focus_limiter(self):
        """ 
        Limite the self.focus to point to the self.grid limits
        Avoiding indexing non-existent objects
        """
        if self.focus[0] < 0:
            self.focus[0] = 0
        elif self.focus[0] > len(self.grid)-1:
            self.focus[0] = len(self.grid)-1
        
        if self.focus[1] < 0:
            self.focus[1] = 0
            
        elif self.focus[1] > len(self.grid[self.focus[0]])-1:
            self.focus[1] = len(self.grid[self.focus[0]])-1
        self.object['x'] = self.focus[1]
        
    def in_grid(self, obj):
        """
        Read the grid in search of 'obj'
        used from 'self.mouse_select' defines the focus object
        Bool return
        """
        for c in self.grid:
            for r in c:
                if r == obj:
                    self.focus = [self.grid.index(c), c.index(r)]# Define the keys from object
                    return True
        return False

    def key_select(self):
        """
        Apply navigation using keyboard(WASD, arrows) and joystick dpad
        """ 
        UP = self.keyboard.activated('w') or self.keyboard.activated(self.keyboard.arrow_key('up')) or self.gamepad.released('up')
        DOWN = self.keyboard.activated('s') or self.keyboard.activated(self.keyboard.arrow_key('down')) or self.gamepad.released('down')
        LEFT = self.keyboard.activated('a') or self.keyboard.activated(self.keyboard.arrow_key('left')) or self.gamepad.released('left')
        RIGHT = self.keyboard.activated('d') or self.keyboard.activated(self.keyboard.arrow_key('right')) or self.gamepad.released('right')
        
        if UP: self.focus[1] -= 1
        elif DOWN: self.focus[1] += 1
        elif LEFT: self.focus[0] -= 1
        elif RIGHT: self.focus[0] += 1
        
        self._focus_limiter()
        self.button_focus = self.grid[self.focus[0]][self.focus[1]]
        self.mouse_active = False # Deactivate the mouse to avoid interfering with navigation


    def mouse_select(self):
        """
            Verify mouse movement to reactivate it 
            get the hovered object and verify in grid to define focus object.
        """
        if self.mouse.on_movement(0.001):
            self.mouse_active = True
        else:
            self.mouse_active = False
            return
         
        if not self.mouse_active:
            return
        
        hovered = self._validate_button(self.mouse.hover())
        
        if hovered:
            if self.in_grid(hovered):
                self.button_focus = self.grid[self.focus[0]][self.focus[1]]
            else:
                self.button_focus = hovered

    
    def _validate_button(self, obj):
        """Verify is a valid button"""
        if not obj:
            return False
        
        button = obj.groupObject if obj.groupObject else obj
        
        if 'button' not in obj:
            return False
        
        # TODO:remove this line once the [settings support gamepad] is live.
        if 'setting' in button and button['setting'] == 'set':
            return
        
        return button
    

    def _get_button_action(self, button):
        """
        Get the button function:
            
        command -> if your button triggers a specifc menu command (ex: "start", "back", "restart", etc...) 
            add the "command" property with the command value (any key name from the self.commands_dict)
        
        set_scene -> if your button accesses a specific scene, add "set scene" property with the specific scene name.
        
        """
        command = button.get('command')
        set_scene = button.get('set scene')
        
        if not command and not set_scene:
            print(f'{button.name}: [WARNING] Any function defined:\n'
                  f'Define "command" or "set scene"')
            return None, None
        
        if command:
            if not isinstance(command, str):
                print(f'{button.name}: [ERROR] "command" must be a STRING')
                return None, None
            command = command.lower().strip()
        
        # Valida set_scene
        if set_scene:
            if not isinstance(set_scene, str):
                print(f'{button.name}: [ERROR] "set scene" must be a STRING')
                return None, None
            set_scene = set_scene.strip()
        
        return command, set_scene
    
    
    def _update_previous(self):   
        """
        Define the current scene as the 'previous scene' from global dict.
        this allow the 'back' function to back this scene.
        """
        if self.object and self.object.scene:
            bge.logic.globalDict['previous menu'] = self.object.scene.name
            bge.logic.saveGlobalDict()

    # ======================= Generic Menu Functions ==============================
    
    def play(self):
        bge.logic.globalDict['previous menu'] = '' # Preventing back to menu where player press esc in pause menu 
        if self.game:
            self.menu.change(self.game)
        else:
            print('no defined game scene')
    
    def quit(self):
        bge.logic.globalDict['previous menu'] = '' 
        bge.logic.saveGlobalDict()
        bge.logic.endGame()
    
    def resume(self):
        for scene in bge.logic.getSceneList():
            if scene.name == self.game:
                scene.resume()
                self.object.scene.end()
                return
        
        print('no defined game scene')
    
    # ======================= Update Loop ==============================
    
    def update(self):
        """
        Apply the button focus function and others menu basics funtionality
        """
        self.mouse_select()
        self.key_select()
        
        button = self.button_focus
        
        # Define the cancel function from gamepad and keyboard
        if self.gamepad.released('b') or self.keyboard.activated('esc') or self.gamepad.released('start'):
            if self.object.scene.name == "Pause":
                self.resume()
                return
            
            elif bge.logic.globalDict.get('Previous menu') != '':
                self.menu.back()
        
        # Define the accept function from gamepad, keyboard and mouse
        if button:
            if (self.mouse.hover(prop='button') and self.mouse.click()) or self.keyboard.activated('enter') or self.gamepad.released('A'):
                command, set_scene = self._get_button_action(button)
                
                if 'setting' in button:
                    return
                if not command and not set_scene:
                    return
                
                if command:
                    if command in self.commands_dict:
                        self.commands_dict[command]()
                
                elif set_scene:
                    scene = set_scene.title()
                    self.menu.change(scene)
