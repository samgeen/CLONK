'''
Created on 25 Aug 2013

@author: samgeen
'''

import Image, pyglet
import numpy as np
import zsprite

from Defines import channels, fontname

def ColHash(r,g=None,b=None):
    if g == None and b == None:
        a = r[3]
        b = r[2]
        g = r[1]
        r = r[0]
    return r*256*256 + g * 256 + b

grey = color=(100,100,100,100)

class Entity(object):
    '''
    A moveable entity in the game world
    '''
    def __init__(self, x,y, vx,vy):
        self._x = x
        self._y = y
        self._vx = vx
        self._vy = vy

class World(object):
    '''
    The world and all in it
    '''


    def __init__(self,size):
        '''
        Constructor
        '''
        self._size = size
        self._names = channels
        self._sprites = []
        self._entities = []
        self._bkg = pyglet.graphics.OrderedGroup(0)
        self._frg = pyglet.graphics.OrderedGroup(1)
        self._Build()
        
    def _Build(self):
        for name in self._names:
            cx,cy = self._size
            x = np.random.randint(0,cx)
            y = np.random.randint(0,cy)
            fontsize = np.random.randint(50,100)
            sprite = pyglet.text.Label(text=r"#"+name,x=x,y=y,
                                           font_name=fontname,font_size=fontsize,
                                           bold=True,
                                           anchor_x='center',anchor_y='center',
                                           color=grey,group=self._bkg)
            self._sprites.append(sprite)
    
    def Run(self, dt):
        for entity in self._entities:
            entity.Move(dt)
            
    def AddEntity(self, entity):
        self._entities.append(entity)
            
    def Scroll(self):
        for sprite in self._sprites:
            # HERE WE NEED TO SCROLL ALL BACKGROUND OBJECTS
            pass
                    
    def Draw(self):
        for sprite in self._sprites:
            sprite.draw()
        for entity in self._entities:
            entity.Draw()
        