'''
Created on 25 Aug 2013

@author: samgeen
'''

import pyglet, zsprite
import numpy as np

from Defines import fontname


class PlayerSprite(object):
    
    def __init__(self, x=0, y=0,angle=0):
        self.x = x
        self.y = y
        self._angle = angle
        self._headoff = 50
        self._sprites = list()
        self._batch = pyglet.graphics.Batch()
        pyglet.resource.path = ['data']
        pyglet.resource.reindex()
        #bigfont = pyglet.font.load(fontname, 40,bold=False) 
        #smallfont = pyglet.font.load(fontname, 20,bold=False)
        #self._body = pyglet.font.Text(bigfont, aman,x=x,y=y,halign='center',valign='center',color=black)
        self._images = dict()
        self._images[False] = pyglet.resource.image("amirite.png")
        self._images[True] = pyglet.resource.image("urnotrong.png")
        self._body = zsprite.ZSprite(self._images[False],x,y,z=10,
                                            batch=self._batch,
                                            subpixel=True)
        scale = 0.5
        self._powered = False
        self._body.scale = scale
        self.width = self._body.width
        self.height = self._body.height
        self._images[False].anchor_x = (self._images[False].width-100)
        self._images[False].anchor_y = self._images[False].height/2
        self._images[True].anchor_x = (self._images[True].width-100)
        self._images[True].anchor_y = self._images[True].height/2
        self._sprites.append(self._body)
        self.Rotate(1,0)
        
    def Move(self, dx, dy):
        self.x += dx
        self.y += dy
        for sprite in self._sprites:
            sprite.x = self.x
            sprite.y = self.y+self._headoff
        self._body.y = self.y
        
    def Rotate(self, x,y):
        angle = np.arctan2(x,y)
        self._angle = angle
        self._body.rotation = angle*180/np.pi - 90
            
    def BodyExtents(self):
        return (self._body.x, self._body.x+self._body.width, self._body.y, self._body.y+self._body.height)
            
    def Draw(self):
        self._body.image = self._images[self._powered]
        if np.random.rand() > 0.5:
            self._body.image = self._images[False]
        self._batch.draw()
        
    def Powered(self, state):
        self._powered = state
        
    def Angle(self):
        return self._angle
            
class Movement(object):
    def __init__(self, x, y, v, sprite, world):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.acc = 10.0
        self._sprite = sprite
        self._world = world
        self._powered = False
        self._angle = 0
        
    def Move(self, timestep):
        self._angle = np.pi/2.0-self._sprite.Angle()
        #self._Collide(vel)
        if self._powered:
            self.vx += self.acc*np.cos(self._angle)
            self.vy += self.acc*np.sin(self._angle)
        dx = self.vx*timestep
        dy = self.vy*timestep
        self.x += dx
        self.y += dy
        self._sprite.Move(dx,dy)
    
    def _Collide(self, vel):
        x0, x1, y0, y1 = self._sprites.BodyExtents()
        self._CollideBox(x0,y0,vel)
        self._CollideBox(x0,y1,vel)
        self._CollideBox(x1,y0,vel)
        self._CollideBox(x1,y1,vel)
        
        
    def _CollideBox(self, b1, b2, vel):
        if self._world.SolidAtPosition(b1+vel[0],b2+vel[1]):
            if self._world.SolidAtPosition(b1+vel[0],b2):
                vel[0] = 0
            if self._world.SolidAtPosition(b1,b2+vel[1]):
                vel[1] = 0
        
    def OnKeyboard(self, state):
        '''
        Register the pressing or releasing of a keyboard key
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        key = pyglet.window.key
        if state["button"] == key.UP or state["button"] == key.W:
            self._powered = state["pressed"]
            self._sprite.Powered(state["pressed"])


class Player(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        x, y, v = (64*26,64*26,300.0)
        self._sprite = PlayerSprite(x,y)
        self._movement = Movement(x, y, v, self._sprite, None)
        self._mode = "hunt"
        self._gruelmasterpos = np.array((x, y-64*2))
    
    def Position(self,centred=False):
        if not centred:
            return (self._sprite.x,self._sprite.y)
        else:
            return (self._sprite.x+self._sprite.width,self._sprite.y+self._sprite.height)
    
    def Mode(self):
        return self._mode
    
    def Draw(self):
        self._sprite.Draw()
    
    def Move(self, timestep):
        self._movement.Move(timestep)
        
    def Rotate(self,x,y):
        self._sprite.Rotate(x,y)
        
    def OnKeyboard(self, state):
        self._movement.OnKeyboard(state)
