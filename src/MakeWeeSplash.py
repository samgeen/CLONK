'''
Created on 25 Apr 2013

@author: samgeen
'''

import Level
import pyglet
import numpy as np

white = color=(1.0,1.0,1.0,1.0)
red = color=(1.0,0.0,0.0,1.0)
black = color=(0.0,0.0,0.0,1.0)
        
class MakeWeeSplash(Level.Level):
    '''
    I am five years old. That is the number of years old I am.
    '''

    def __init__(self, nextLevel):
        '''
        Constructor
        nextLevel - Level object to pass to the screen next
        '''
        Level.Level.__init__(self)
        self._nextLevel = nextLevel
        self._time = 0.0
        self._mwTime = 6.0 # seconds
        self._sequence = ["MakeWee","Title"]
        self._sequence = 0
        self._makeweetext = None
        self._title = None
        self._clicktobegin = None
        #self._bgimage = "twist_back.jpg"
        #self._background = None
        #self._boff = (0,0)
        
    def Setup(self):
        '''
        Set up the splash screen
        '''
        # Set up general text stuff
        # Use default font
        pyglet.resource.path = ['data']
        pyglet.resource.reindex()
        fontname = "Lato-Regular"
        bigfont = pyglet.font.load(fontname, 40,bold=False) 
        smallfont = pyglet.font.load(fontname, 20,bold=False)
        cx, cy = self.Window().get_size()
        cx /= 2
        cy /= 2
        # MakeWee text
        text = "A MakeWee Games Production"
        self._makeweetext = pyglet.font.Text(bigfont, text,x=cx,y=cy,halign='center',valign='center',color=black)
        # Title text
        text = "CLONK"
        self._title = pyglet.font.Text(bigfont, text,x=cx,y=cy,halign='center',valign='center',color=black)
        text = "Click to Begin"
        self._clicktobegin = pyglet.font.Text(smallfont, text,x=cx,y=40,halign='center',valign='baseline',color=black)
        # Background
        #bgimage = pyglet.resource.image(self._bgimage)
        #self._background = pyglet.sprite.Sprite(bgimage,subpixel="True")
        #self._boff = (-self._background.width/2+cx, -self._background.height/2+cy-100)
        
        
    def Run(self, timestep):
        '''
        Run for a single timestep
        '''
        # Increment timer
        self._time += timestep
        # Draw background
        #btime = np.min([self._time, 3*60])
        #bpos = - btime / 1000.0 * np.array([self._background.width, self._background.height])
        #bx, by = bpos
        #self._background.x = bx+self._boff[0]
        #self._background.y = by+self._boff[1]
        #self._background.draw()
        pyglet.gl.glClearColor(1,1,1,1)
        # Change level?
        if self._time >= self._mwTime:
            self._sequence = 1
        if self._sequence == 0:
            self._makeweetext.draw()
        elif self._sequence == 1:
            self._title.draw()
            self._clicktobegin.draw()
        
    def _Skip(self):
        '''
        Skip to next screen
        '''
        self._sequence += 1
        if self._sequence > 1:
            self.ChangeLevel(self._nextLevel)
        
    def OnMouseButton(self, button):
        if button["pressed"] == True:
            self._Skip()
        
    def OnKeyboard(self, state):
        self._sequence = 1  