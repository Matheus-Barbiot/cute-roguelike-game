#icon=COLOR
import bge

class Background:
    def __init__(self, background):
        self.background = background
        self.scene = bge.logic.getCurrentScene()
        
    def load(self, replace=True):
        if self.background != '':
            current = bge.logic.getSceneList()[0]

            if replace and current.name != self.scene.name and current.name != self.background:
                current.replace(self.background)
                return

            bge.logic.addScene(self.background, False)