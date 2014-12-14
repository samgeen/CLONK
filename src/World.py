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

def label2texture(label):
    vertex_list = label._vertex_lists[0].vertices[:]
    xpos = map(int, vertex_list[::8])
    ypos = map(int, vertex_list[1::8])
    glyphs = label._get_glyphs()

    xstart = xpos[0]
    xend = xpos[-1] + glyphs[-1].width
    width = xend - xstart

    ystart = min(ypos)
    yend = max(ystart+glyph.height for glyph in glyphs)
    height = yend - ystart

    texture = pyglet.image.Texture.create(width, height,
pyglet.gl.GL_ALPHA)

    for glyph, x, y in zip(glyphs, xpos, ypos):
        data = glyph.get_image_data()
        x = x - xstart
        y =  height - glyph.height - y + ystart
        texture.blit_into(data, x, y, 0)

    return texture 

class Entity(object):
    '''
    A moveable entity in the game world
    '''
    def __init__(self, x,y, vx,vy):
        self._x = x
        self._y = y
        self._vx = vx
        self._vy = vy
        
class Clonked(object):
    
    
    pyglet.resource.path = ['data']
    pyglet.resource.reindex()
    image = pyglet.resource.image("clonk2.png")
    image.anchor_x = image.width//2
    image.anchor_y = image.height//2
    cooldown = 0.5
    
    def __init__(self, x,y,vx,vy,world):
        batch = world.ForeBatch()
        sprite = pyglet.sprite.Sprite(self.image,x=x,y=y,batch=batch)
        self._moveable = Player.Moveable(x, y, sprite, world, vx=vx, vy=vy, acc=100.0,angle=0.0,fric=0.0)
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

class Asteroid(object):
    
    names = ["RPS","DAN","HIM"]
    _images = dict()
    
    def __init__(self, world,static=False,name=None,first=False):
        self._world = world
        if name is None:
            self._name = np.random.choice(self.names)
        else:
            self._name = name
        self._static = static
        # Set positional information
        cx,cy = world.WindowSize()
        px,py = world.Player().Position(centred=True)
        speed = 50.0
        fontsize = np.random.randint(30,70)
        colour = black
        batch = world.ForeBatch()
        minrange = 1.0
        if static:
            speed = 0.0
            fontsize = np.random.randint(70,150)
            colour = grey
            batch = world.BackBatch()
            if first:
                minrange = 0.0
        angle = np.random.rand()*np.pi*2.0
        theta = np.random.rand()*2.0*np.pi
        r = 4.0*np.random.rand()+minrange
        r *= max(cx,cy)
        x  = r*np.cos(theta)+px
        y  = r*np.sin(theta)+py
        vx = np.cos(angle)*speed
        vy = np.sin(angle)*speed
        # Make sprite
        if not self._name in self._images:
            pyglet.resource.path = ['data/labels']
            pyglet.resource.reindex()
            im = pyglet.resource.image(self._name+".png")
            im.anchor_x = im.width//2
            im.anchor_y = im.height//2
            self._images[self._name] = im
            #label = pyglet.text.Label(text=self._name,x=0,y=0,
            #                       font_name=fontname,font_size=fontsize,
            #                       bold=True,
            #                       #anchor_x='center',anchor_y='center',
            #                       color=colour)
            #self._images[self._name] = self._ImFromLabel(label)
        self._sprite = pyglet.sprite.Sprite(self._images[self._name],x=x,y=y,batch=batch)
        self._moveable = Player.Moveable(x,y,self._sprite,self._world,vx,vy,angle=0.0)
        self._collision = collide.SpriteCollision(self._sprite)
        
    def _ImFromLabel(self,label):
        # DEPRECATED, USED FOR INITIAL GENERATION ONLY
        vertex_list = []
        for vl in label._vertex_lists:
            vertex_list = vertex_list+vl.vertices[:]
        #vertex_list = label._vertex_lists[0].vertices[:]
        xpos = map(int, vertex_list[::8])
        ypos = map(int, vertex_list[1::8])
        glyphs = label._get_glyphs()
    
        xstart = xpos[0]
        xend = xpos[-1] + glyphs[-1].width
        #width = xend - xstart
        
        width = label.content_width
        height = label.content_height
    
        ystart = min(ypos)
        yend = max(glyph.height for glyph in glyphs)
        #height = yend - ystart
        
        texture = pyglet.image.Texture.create(width, height, pyglet.gl.GL_RGBA)
    
        for glyph, x, y in zip(glyphs, xpos, ypos):
            data = glyph.get_image_data()
            x = x - xstart
            y =  height - glyph.height - y + ystart # TODO FIGURE OUT WHY THIS IS BUGGED
            texture.blit_into(data, x, y, 0)
            
        texture.anchor_x = texture.width//2
        texture.anchor_y = texture.height//2
        
        texture = texture.get_transform(flip_y=True)
        
        texture.save("data/labels/"+label.text+".png")
    
        return texture 
        
    def Draw(self):
        self._moveable.Draw()
        
        
    def Move(self,dt):
        self._moveable.Move(dt)
        
    def CheckInWorld(self):
        cx,cy = self._world.WindowSize()
        px,py = self._world.Player().Position(centred=True)
        if (self._sprite.x - px)**2 + (self._sprite.y - py)**2 > \
            (cx**2 + cy**2)*16:
            #print (self._sprite.x - px)**2 + (self._sprite.y - py)**2, (cx**2 + cy**2)*16
            # Kill and replace
            self._world.MakeRoid(self._name,self._static,tokill=self)
            
    def Clonk(self):
        self._world.AddEntity(Clonked(self._moveable.x,
                                      self._moveable.y,
                                      self._moveable.vx,
                                      self._moveable.vy,
                                      self._world))
        
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

    def __init__(self,winsize, maingame):
        '''
        Constructor
        '''
        self._winsize = winsize
        self._maingame = maingame
        self._player = None
        self._names = channels
        self._passives = []
        self._entities = {}
        self._entities[Asteroid] = []
        self._explain = pyglet.text.Label(text="WSAD & Mouse to move, Space / LMB to fire, Clonk you-know-who",
                                          x=0,y=-100,
                                          font_name=fontname,
                                          font_size=26,
                                          color=black,anchor_x="center",anchor_y="center")
        self._bkg = pyglet.graphics.Batch()
        self._frg = pyglet.graphics.Batch()
        self._Build()
    
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
            #x = np.random.randint(0,cx)
            #y = np.random.randint(0,cy)
            #fontsize = np.random.randint(50,100)
            #sprite = pyglet.text.Label(text=r"#"+name,x=x,y=y,
            #                               font_name=fontname,font_size=fontsize,
            #                               bold=True,
            #                               anchor_x='center',anchor_y='center',
            #                               color=grey,group=self._bkg)
            self.MakeRoid("#"+name,static=True,first=True)
    
    def MakeRoid(self, name,static,first=False,tokill=None):
        roid = Asteroid(self,static=static,name=name,first=first)
        if tokill:
            tokill.Kill()
        if static:
            if tokill:
                self._passives.remove(tokill)
            self._passives.append(roid)
            
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
                            if clonk.IsAlive() and roid.IsAlive():
                                roid.Clonk()
                                self._maingame.Score().AddScore()
                                roid.Kill()
                                clonk.Kill()
            # Collide player with asteroids
            for roid in roids:
                if collide.collide(roid.Collision(), self._player.Collision()):
                    roid.Kill()
                    self._maingame.DieScreen()
                    self._player.Kill()
    
    def Run(self, dt):
        for entity in self._IterEntities():
            # Move entities
            entity.Move(dt)
        # Add entity
        numroids = len(self._entities[Asteroid])
        diff = self.MAXROIDS - numroids
        for i in range(0,diff):
            # Make a new one on average every 0.1 second until we hit the maximum
            #if 0.1*np.random.rand() < dt:
            # TODO: PREVENT THIS TELEPORT-CRUSHING THE PLAYER
            self.AddEntity(Asteroid(self))
        # Collide entities
        self.Collide()
        # Check in world
        for roid in self._entities[Asteroid]:
            roid.CheckInWorld()
        for roid in self._passives:
            roid.CheckInWorld()
        # Clean up dead objects
        nent = 1
        for entity in self._IterEntities():
            nent += 1
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
        entity.Sprite().delete()
        self._entities[etype].remove(entity)
            
    def Scroll(self):
        for sprite in self._sprites:
            # HERE WE NEED TO SCROLL ALL BACKGROUND OBJECTS
            pass
        
    def Player(self):
        return self._player
                    
    def Draw(self):
        # Prep objects for rendering
        #for passive in self._passives:
        #    passive.Draw()
        #for entity in self._IterEntities():
        #    entity.Draw()
        # Draw batches
        self._bkg.draw()
        self._explain.draw()
        self._frg.draw()
        