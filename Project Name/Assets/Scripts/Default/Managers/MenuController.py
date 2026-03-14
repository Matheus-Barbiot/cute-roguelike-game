#icon=SCRIPTWIN
import bge


class MenuController:
    """
    MenuController is a generic menu navigation controller.
    It is designed to be used together with the Menu component (logic_menu.py).
    """

    def __init__(self, home='', previous='', next=''):
        self.scenes = bge.logic.getSceneList() + bge.logic.getInactiveSceneNames()
        self.current = bge.logic.getCurrentScene()

        self.home = home
        self.previous = previous
        self.next = next

    # ---------------- Navigation Methods ---------------- #

    def back(self):
        """Return to the previous menu scene."""
        if self.is_valid(self.previous):
            self._replace(self.previous)

    def advance(self):
        """Go to the next menu scene."""
        if self.is_valid(self.next):
            self._replace(self.next)

    def change(self, scene=''):
        """Change to a specific scene."""
        if self.is_valid(scene):
            self._replace(scene)

    def return_home(self):
        """Return to the home menu scene."""
        if self.is_valid(self.home):
            self._replace(self.home)

    # ---------------- Internal Methods ---------------- #

    def _replace(self, scene_name):
        """Replace the current scene with the given scene name."""
        try:
            self.current.replace(scene_name)
        except Exception as e:
            print(f'[ERROR] Failed to switch to "{scene_name}": {e}')

    def is_valid(self, scene):
        """
        Validate whether a scene name exists and can be used.

        :param scene: Scene name to validate
        :return: True if valid, False otherwise
        """
        if scene is None:
            print('[ERROR] Scene is None')
            return False

        if not isinstance(scene, str):
            print(f'[ERROR] Scene name is not a string: {type(scene).__name__}')
            return False

        if not scene.strip():
            print('[ERROR] Scene name is empty')
            return False

        for s in self.scenes:
            scene_name = s.name if hasattr(s, 'name') else str(s)
            if scene == scene_name:
                return True

        print(f'[ERROR] Scene "{scene}" not found')
        return False