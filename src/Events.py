'''
Created on 8 May 2013

@author: samgeen
'''

'''
A module listing all events used by the game with some convenience functions
'''

class UserInputHandler(object):
    '''
    Handles user input from mouse and keyboard
    '''
    def __init__(self, level):
        # Use pyglet's inbuilt key state handler (NOTE - MIGHT NOT BE ABLE TO USE MODIFIER KEYS LIKE THIS)
        self._level = level
    
    def on_mouse_press(self, x, y, button, modifiers):
        press = {"pos": (x,y), "button":button, "mod": modifiers, "pressed":True}
        self._level.OnMouseButton(press)

    def on_mouse_release(self, x, y, button, modifiers):
        release = {"pos": (x,y), "button":button, "mod": modifiers, "pressed":False}
        self._level.OnMouseButton(release)

    # NOTE: Functions drag and move merged to make things easier
    def on_mouse_motion(self, x, y, dx, dy):
        motion = {"pos": (x,y), "diff": (dx, dy), "buttons":None, "mod":None}
        self._level.OnMouseMove(motion)
        
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        motion = {"pos": (x,y), "diff": (dx, dy), "buttons":buttons, "mod":modifiers}
        self._level.OnMouseMove(motion)
        
    def on_key_press(self, button, modifiers):
        press = {"button":button, "mod": modifiers, "pressed":True}
        self._level.OnKeyboard(press)

    def on_key_release(self, button, modifiers):
        release = {"button":button, "mod": modifiers, "pressed":False}
        self._level.OnKeyboard(release)
