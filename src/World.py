'''
Created on 25 Aug 2013

@author: samgeen
'''

import Image, pyglet, Player, collide
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

black = color=(0,0,0,255)
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

class Asteroid(object):
    
    names = ["RPS","DAN","HIM"]
    
    def __init__(self, world,static=False,name=None):
        self._world = world
        if name is None:
            self._name = np.random.choice(self.names)
        else:
            self._name = name
        # Set positional information
        cx,cy = world.Size()
        speed = 20.0
        fontsize = np.random.randint(30,70)
        colour = black
        batch = world.ForeBatch()
        if static:
            speed = 0.0
            fontsize = np.random.randint(70,150)
            colour = grey
            batch = world.BackBatch()
        angle = np.random.rand()*np.pi*2.0
        x  = np.random.rand()*cx
        y  = np.random.rand()*cy
        vx = np.cos(angle)*speed
        vy = np.sin(angle)*speed
        # Make sprite
        self._sprite = pyglet.text.Label(text=self._name,x=x,y=y,
                                   font_name=fontname,font_size=fontsize,
                                   bold=True,
                                   anchor_x='center',anchor_y='center',
                                   color=colour,batch=batch)
        self._moveable = Player.Moveable(x,y,self._sprite,self._world,vx,vy,angle=0.0)
        self._collision = collide.SpriteCollision(self._sprite)
        
    def Draw(self):
        self._moveable.Draw()
        
    def Move(self,dt):
        self._moveable.Move(dt)
        
    def IsAlive(self):
        return self._moveable.IsAlive()
        
    def Kill(self):
        return self._moveable.Kill()
    
    def Sprite(self):
        return self._moveable.sprite
    
    def Collision(self):
        return self._collision

class World(object):
    '''
    The world and all in it
    '''

    MAXROIDS = 100

    def __init__(self,size,winsize):
        '''
        Constructor
        '''
        self._size = size
        self._winsize = winsize
        self._player = None
        self._names = channels
        self._passives = []
        self._entities = {}
        self._entities[Asteroid] = []
        self._bkg = pyglet.graphics.Batch()
        self._frg = pyglet.graphics.Batch()
        self._Build()
        
    def Size(self):
        return self._size
    
    def WindowSize(self):
        return self._winsize
    
    def BackBatch(self):
        return self._bkg
    
    def ForeBatch(self):
        return self._frg
        
    def _Build(self):
        # Add player
        self._player = Player.Player(0,0, self)
        # Add passive background objects
        for name in self._names:
            cx,cy = self._size
            #x = np.random.randint(0,cx)
            #y = np.random.randint(0,cy)
            #fontsize = np.random.randint(50,100)
            #sprite = pyglet.text.Label(text=r"#"+name,x=x,y=y,
            #                               font_name=fontname,font_size=fontsize,
            #                               bold=True,
            #                               anchor_x='center',anchor_y='center',
            #                               color=grey,group=self._bkg)
            self._passives.append(Asteroid(self,static=True,name="#"+name))
            
    def Collide(self):
        '''
        Collide stuff
        '''
        # Collide bullets with asteroids
        if Asteroid in self._entities:
            roids = self._entities[Asteroid]
            if Player.Clonk in self._entities:
                for clonk in self._entities[Player.Clonk]:
                    for roid in roids:
                        if collide.collide(roid.Collision(), clonk.Collision()):
                            roid.Kill()
                            clonk.Kill()
            # Collide player with asteroids
            for roid in roids:
                if collide.collide(roid.Collision(), self._player.Collision()):
                    roid.Kill()
                    self._player.Kill()
    
    def Run(self, dt):
        for entity in self._IterEntities():
            # Move entities
            entity.Move(dt)
        # Add entity
        numroids = len(self._entities[Asteroid])
        if numroids < self.MAXROIDS:
            # Make a new one on average every second until we hit the maximum
            if np.random.rand() < dt:
                # TODO: PREVENT THIS TELEPORT-CRUSHING THE PLAYER
                self.AddEntity(Asteroid(self))
        # Collide entities
        self.Collide()
        # Clean up dead objects
        for entity in self._IterEntities():
            if not entity.IsAlive():
                self.KillEntity(entity)
                
    def _IterEntities(self):
        for typelist in self._entities.itervalues():
            for entity in typelist:
                yield entity
            
    def AddEntity(self, entity):
        etype = type(entity)
        if not etype in self._entities:
            self._entities[etype] = [entity]
        else:
            self._entities[etype].append(entity)
            
    def KillEntity(self,entity):
        etype = type(entity)
        self._entities[etype].remove(entity)
            
    def Scroll(self):
        for sprite in self._sprites:
            # HERE WE NEED TO SCROLL ALL BACKGROUND OBJECTS
            pass
        
    def Player(self):
        return self._player
                    
    def Draw(self):
        # Prep objects for rendering
        for passive in self._passives:
            passive.Draw()
        for entity in self._IterEntities():
            entity.Draw()
        # Draw batches
        self._bkg.draw()
        self._frg.draw()
        