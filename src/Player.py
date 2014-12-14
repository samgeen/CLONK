'''
Created on 25 Aug 2013

@author: samgeen
'''

import pyglet, zsprite, collide
import World
import numpy as np

from Defines import fontname

class Clonk(object):
    
    
    pyglet.resource.path = ['data']
    pyglet.resource.reindex()
    image = pyglet.resource.image("clonkman.png")
    cooldown = 2.0
    
    def __init__(self, moveable):
        self._moveable = moveable
        self._life = self.cooldown
        self._sprite = self._moveable.sprite
        self._collision = collide.SpriteCollision(self._sprite)
        
    def Move(self, dt):
        self._life -= dt
        if self._life < 0.0:
            self.Kill()
        else:
            self._moveable.Move(dt)
        
    def Draw(self):
        self._moveable.sprite.draw()
        
    def IsAlive(self):
        return self._moveable.IsAlive()
    
    def Kill(self):
        self._moveable.Kill()
        
    def Sprite(self):
        return self._moveable.sprite
    
    def Collision(self):
        return self._collision

class PlayerSprite(object):
    
    def __init__(self, x=0, y=0,angle=0):
        self.x = x
        self.y = y
        self.rotation = 0.0
        self._angle = angle
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
        self._unpowered = zsprite.ZSprite(self._images[False],x,y,z=10,
                                            batch=self._batch,
                                            subpixel=True)
        scale = 0.5
        self._powered = False
        self._body.scale = scale
        self._unpowered.scale = scale
        self.width = self._body.width
        self.height = self._body.height
        self._images[False].anchor_x = (self._images[False].width-100)
        self._images[False].anchor_y = self._images[False].height/2
        self._images[True].anchor_x = (self._images[True].width-100)
        self._images[True].anchor_y = self._images[True].height/2
            
    def Draw(self):
        self._body.x = self.x
        self._body.y = self.y
        self._body.rotation = self.rotation
        # Make sure unpowered body is always in the right place for collisions
        self._unpowered.x = self.x
        self._unpowered.y = self.y
        self._unpowered.rotation = self.rotation
        self._body.image = self._images[self._powered]
        if np.random.rand() > 0.5:
            self._body.image = self._images[False]
        self._batch.draw()
        
    def Powered(self, power):
        self._powered = power
        
    def UnpoweredSprite(self):
        return self._unpowered
    
    def delete(self):
        '''
        Match pyglet interface
        '''
        self._images[False].delete()
        self._images[True].delete()
            
class Moveable(object):
    def __init__(self, x, y, sprite, world, vx=0.0, vy=0.0, acc=100.0,angle=None,fric=0.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.acc = acc
        self.angle = angle
        self.fric = fric
        self.sprite = sprite
        self._world = world
        self._powered = False
        self._alive = True
        if angle is None:
            if vx != 0.0 or vy != 0.0:
                self.angle = np.arctan2(-vy,vx)
                self.sprite.rotation = self.angle*180/np.pi
            else:
                self.angle = 0.0
                
    def IsAlive(self):
        return self._alive
    
    def Kill(self):
        self._alive = False
        
    def Delete(self):
        self.sprite.delete()
        
    def Rotate(self, x,y):
        self.angle = np.arctan2(-y,x)
        
    def Powered(self, powered):
        self._powered = powered
        self.Move(0.0)
        
    def Move(self, timestep):
        # Accelerate?
        if self._powered:
            self.vx += 0.5*self.acc*np.cos(self.angle)*timestep
            self.vy -= 0.5*self.acc*np.sin(self.angle)*timestep
        # Friction
        self.vx *= 1.0-self.fric*timestep
        self.vy *= 1.0-self.fric*timestep
        # Set timestep
        dx = self.vx*timestep
        dy = self.vy*timestep
        self.x += dx
        self.y += dy
        # Move sprite
        #self._LoopInWorld(self)
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = self.angle*180/np.pi
        
    def Draw(self):
        '''
        px,py : Player coords
        wx,wy : Window size
        '''
        self.sprite.x = self.x
        self.sprite.y = self.y
        px,py = self._world.Player().Position(centred=True)
        wx,wy = self._world.WindowSize()
        sx = wx/2
        sy = wy/2
        ox = self.x
        oy = self.y
        try:
            ow = self.sprite.width/2
            oh = self.sprite.height/2
        except:
            ow = self.sprite.content_width/2
            oh = self.sprite.content_height/2
        # Loop sprite in world to match player view
        #if self.x != px and self.y != py:
        #    self._LoopDraw(cx,cy,px,py,sx,sy,ox,ow,oy,oh)
        #self.sprite.draw()
        
    def _LoopDraw(self,cx,cy,px,py,sx,sy,ox,ow,oy,oh):
        '''
        Draw the object looped so that the player sees objects on the other side of the world
        '''
        if px + sx > cx:
            if ox-ow < sx:
                self.sprite.x += cx
        if py + sy > cy:
            if oy-oh < sy:
                self.sprite.y += cy
        if px < sx:
            if ox+ow > cx-sx:
                self.sprite.x -= cx
        if py < sy:
            if oy+oh > cy-sy:
                self.sprite.y -= cy
        
    def _LoopInWorld(self, obj):
        '''
        Note that obj can be this Moveable or the sprite
        '''
        cx,cy = self._world.Size()
        if obj.x > cx:
            obj.x -= cx
        if obj.x < 0:
            obj.x += cx
        if obj.y > cy:
            obj.y -= cy
        if obj.y < 0:
            obj.y += cy

class Player(object):
    '''
    Player object
    '''

    def __init__(self, x,y,world):
        '''
        Constructor
        '''
        self._world = world
        self._sprite = PlayerSprite(x,y)
        self._movement = Moveable(x, y, self._sprite, self._world,fric=0.2,acc=1e3)
        self._fire = False
        self._cooldown = 0.0
        self._collision = collide.SpriteCollision(self._sprite.UnpoweredSprite())
    
    def Position(self,centred=False):
        if not centred:
            return (self._sprite.x,self._sprite.y)
        else:
            return (self._sprite.x+self._sprite.width,self._sprite.y+self._sprite.height)
        
    def Velocity(self):
        return self._movement.vx, self._movement.vy
    
    def Draw(self):
        self._sprite.Draw()
        
    def _Fire(self, dt):
        # Fire weapon?
        if self._fire:
            if self._cooldown <= 0.0:
                x  = self._movement.x
                y  = self._movement.y
                vx = self._movement.vx
                vy = self._movement.vy
                cvel = 800.0
                vx += cvel * np.cos(self._movement.angle)
                vy -= cvel * np.sin(self._movement.angle)
                batch = self._world.ForeBatch()
                clonksprite = zsprite.ZSprite(Clonk.image,x,y,z=11,
                                            subpixel=True,batch=batch)
                clonksprite.scale = 0.25
                moveable = Moveable(x,y,clonksprite,self._world,vx,vy,angle=self._movement.angle)
                entity = Clonk(moveable)
                self._world.AddEntity(entity)
                self._cooldown = 0.4
    
    def Move(self, timestep):
        # Move
        self._movement.Move(timestep)
        # Fire?
        self._cooldown -= timestep
        self._Fire(timestep)
        
    def Rotate(self,x,y):
        self._movement.Rotate(x,y)
        
    def OnMouseButton(self, state):
        '''
        Register the pressing or releasing of a mouse button
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"pos": (x,y), "button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        if state["button"] == pyglet.window.mouse.LEFT:
            self._fire = state["pressed"]
        
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
            self._movement.Powered(state["pressed"])
            self._sprite.Powered(state["pressed"])
        if state["button"] == key.SPACE:
            self._fire = state["pressed"]
            
    def Sprite(self):
        return self._sprite.UnpoweredSprite()
    
    def Collision(self):
        return self._collision

    def Kill(self):
        print "URDEAD"

