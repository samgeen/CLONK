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

class World(object):
    '''
    classdocs
    '''


    def __init__(self,size):
        '''
        Constructor
        '''
        self._size = size
        self._names = channels
        self._sprites = []
        self._bkg = pyglet.graphics.Batch()
        self._Build()
        
    def _Build(self):
        for name in self._names:
            cx,cy = self._size
            x = np.random.randint(0,cx)
            y = np.random.randint(0,cy)
            fontsize = np.random.randint(50,100)
            sprite = pyglet.text.Label(text=r"#"+name,x=x,y=y,
                                           font_name=fontname,font_size=fontsize,
                                           anchor_x='center',anchor_y='center',
                                           color=grey,batch=self._bkg)
            self._sprites.append(sprite)
            
    def Scroll(self):
        for sprite in self._sprites:
            # HERE WE NEED TO SCROLL ALL BACKGROUND OBJECTS
            pass
                    
    def Draw(self):
        self._bkg.draw()
        