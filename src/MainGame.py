'''
Created on 25 Apr 2013

@author: samgeen
'''

import Level, zsprite, EndScreen, Player, World

import pyglet
from pyglet.gl import * # it already has the gl prefix so OK whatevs

import random
import numpy as np
from Defines import fontname

smallfont = pyglet.font.load(fontname, 14)
white = color=(1.0,1.0,1.0,1.0)
red   = color=(1.0,0.0,0.0,1.0)
black = color=(0.0,0.0,0.0,1.0)
    
class Score(object):
    def __init__(self):
        self._mode = "hunt"
        self._score = 0
        self._scoretext = None
        self._xoff = 0
        self._yoff = 0
        
    def Setup(self, width, height):
        pyglet.resource.path = ['data']
        pyglet.resource.reindex()
        bigfont = pyglet.font.load(fontname, 64,bold=False)
        self._scoretext = pyglet.font.Text(bigfont, str(self._score),
                                          x=width - 64*2,y=height-128,z=200,color=black)
        
    def OffsetDraw(self, x, y):
        self._xoff = x
        self._yoff = y
        
    def AddScore(self):
        self._score += 1
        self._scoretext.text = str(self._score)
        
    def Score(self):
        return self._score
    
    def Mode(self, mode):
        self._mode = mode
    
    def Draw(self):
        self._scoretext.text = str(self._score)
        self._DrawItem(self._scoretext)
            
    def _DrawItem(self, sprite):
        x = sprite.x
        y = sprite.y
        sprite.x += self._xoff
        sprite.y += self._yoff
        sprite.draw()
        sprite.x = x
        sprite.y = y
    
class MainGame(Level.Level):
    '''
    The main game level
    '''

    def __init__(self):
        '''
        Constructor
        '''
        Level.Level.__init__(self)
        self._winScreen = EndScreen.EndScreen()
        self._score = None
        self._player = None
        self._world = None
        
    def Setup(self):
        '''
        Set up the main level
        '''
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)
        cx, cy = self.Window().get_size()
        self._score = Score()
        self._score.Setup(cx, cy)
        size = (cx*4,cy*4)
        self._world = World.World(size,self.Window().get_size())
        self._player = self._world.Player()
        
    def Run(self, timestep):
        '''
        Run for a single timestep
        '''
        # Run
        pyglet.gl.glClearColor(1,1,1,1)
        self._player.Move(timestep)
        self._world.Run(timestep)
        # Scroll window
        x, y = self._player.Position()
        cx, cy = self.Window().width, self.Window().height
        self.Window().ScrollTo(x-cx/2,y-cy/2)
        # Score
        x,y = (0,0)
        self._score.OffsetDraw(x-cx/2,y-cy/2)
        #if self._urchin.AskForMore():
        self._score.AddScore()
        # Draw
        self._world.Draw()
        self._score.Draw()
        self._player.Draw()
        '''
        self._world.Draw()
        self._disguises.Draw()
        # Have we won yet? IF NOT WHY NOT
        if self._score.Score() >= 11:
            self.Window().ChangeLevel(self._winScreen)
        '''
        
    def OnMouseButton(self, state):
        '''
        Parse mouse clicks
        '''
        if state["button"] == pyglet.window.mouse.LEFT and state["pressed"] == True:
            pass
        
    def OnMouseMove(self, state):
        '''
        Parse mouse movement
        state - a dictionary of the mouse state:
                   {"pos": (x,y), "button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        x,y = state["pos"]
        cx, cy = self.Window().width, self.Window().height
        x -= cx/2
        y -= cy/2
        self._player.Rotate(x,y)
        
    def OnMouseButton(self, state):
        '''
        Register the pressing or releasing of a mouse button
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"pos": (x,y), "button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        self._player.OnMouseButton(state)
        

    def OnKeyboard(self, state):
        '''
        Register the pressing or releasing of a keyboard key
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        self._player.OnKeyboard(state)
