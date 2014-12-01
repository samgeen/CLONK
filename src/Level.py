'''
Created on 24 Apr 2013

@author: samgeen
'''

import abc
import pyglet
from pyglet.gl import * # it already has the gl prefix so OK whatevs
import Events

import pyglet.window.mouse as mouse
import pyglet.window.key as key
    
class LevelChanger(pyglet.event.EventDispatcher):
    def ChangeLevel(self):
        self.dispatch_events('on_change_level')
        
LevelChanger.register_event_type('on_change_level')

class Level(object):
    '''
    A level; contains a backdrop, game logic director, etc
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
        self._window = None
        self._nextLevel = None
        self._userInput = None
        self._setup = False
        
    def SetupWindow(self, window):
        '''
        Sets up the window in the level
        '''
        # Prevent weird repeat setups
        if not self._setup:
            self._userInput = Events.UserInputHandler(self)
            window.push_handlers(self._userInput)
            self._window = window
            glDisable(GL_DEPTH_TEST)
            self.Setup()
            self._setup = True
        
    def Window(self):
        '''
        Get the current window instance
        '''
        return self._window
    
    @abc.abstractmethod
    def Setup(self):
        '''
        Setup the level
        ABSTRACT METHOD; MUST BE ADDED BY CONCRETE CLASS
        '''
        return
    
    @abc.abstractmethod
    def Run(self, dtime):
        '''
        Run the level for one timestep
        ABSTRACT METHOD; MUST BE ADDED BY CONCRETE CLASS
        '''
        return
        
    def ChangeLevel(self, nextLevel):
        '''
        Change to the next level
        Normally called by the concrete class
        '''
        #lc = LevelChanger()
        #self._window.push_handlers(self.Window())
        self.Window().ChangeLevel(nextLevel)
        
    # EVENT HANDLERS
    def OnMouseButton(self, state):
        '''
        Register the pressing or releasing of a mouse button
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"pos": (x,y), "button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        pass
    
    def OnMouseMove(self, state):
        '''
        Register the motion of the mouse
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"pos": (x,y), "button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        pass
    
    def OnKeyboard(self, state):
        '''
        Register the pressing or releasing of a keyboard key
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        pass
        