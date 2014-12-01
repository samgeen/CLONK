'''
Created on 25 Apr 2013

@author: samgeen
'''

import Level
import numpy as np
import pyglet, zsprite
from pyglet.gl import * # it already has the gl prefix so OK whatevs
    
white = color=(1.0,1.0,1.0,1.0)
red   = color=(1.0,0.0,0.0,1.0)
black = color=(0.0,0.0,0.0,1.0)

class EndScreen(Level.Level):
    '''
    End game screen
    '''

    def __init__(self):
        '''
        Constructor
        nextLevel - Level object to pass to the screen next
        '''
        Level.Level.__init__(self)
        self._time = 0.0
        self._mwTime = 6.0 # seconds
        self._sequence = ["MakeWee","Title"]
        self._sequence = 0
        self._makeweetext = None
        self._title = None
        self._clicktobegin = None
        self._bgimage = "twist_back.jpg"
        self._background = None
        self._boff = (0,0)
        
    def Setup(self):
        '''
        Set up the splash screen
        '''
        # Set up general text stuff
        # Use default font
        self.Window().ScrollTo(0,0)
        bigfont = pyglet.font.load("Palatino", 40,bold=True) 
        smallfont = pyglet.font.load("Palatino", 20,bold=True)
        cx, cy = self.Window().get_size()
        cx /= 2
        cy /= 2
        # MakeWee text
        text = "~ FIN ~"
        self._makeweetext = pyglet.font.Text(bigfont, text,x=cx,y=cy,halign='center',valign='center',color=red)
        # Title text
        text = "1+10 More"
        self._title = pyglet.font.Text(bigfont, text,x=cx,y=cy,halign='center',valign='center',color=red)
        text = "Click to Begin"
        self._clicktobegin = pyglet.font.Text(smallfont, text,x=cx,y=40,halign='center',valign='baseline',color=red)
        # Background
        pyglet.resource.path = ['data']
        pyglet.resource.reindex()
        bgimage = pyglet.resource.image(self._bgimage)
        self._background = pyglet.sprite.Sprite(bgimage,subpixel="True")
        self._boff = (-self._background.width/2+cx, -self._background.height/2+cy-100)
        
        
    def Run(self, timestep):
        '''
        Run for a single timestep
        '''
        # Increment timer
        self._time += timestep
        # Draw background
        btime = np.min([self._time, 3*60])
        bpos = - btime / 1000.0 * np.array([self._background.width, self._background.height])
        bx, by = bpos
        self._background.x = bx+self._boff[0]
        self._background.y = by+self._boff[1]
        self._background.draw()
        # Change level?
        self._makeweetext.draw()
        
    def OnMouseButton(self, button):
        pass
        
    def OnKeyboard(self, state):
        pass