'''
Created on 25 Aug 2013

@author: samgeen
'''

import random, pyglet, zsprite

ordering = {"hat": 8,
            "pinkwig": 5,
            "rednose": 10,
            "faketan": 2,
            "glasses": 9,
            "beard": 3,
            "arrow": 7,
            "ruff": 1,
            "sideburns": 4,
            "moustache": 6}

disguises = ["hat",
            "pinkwig",
            "rednose",
            "faketan",
            "glasses",
            "beard",
            "arrow",
            "ruff",
            "sideburns",
            "moustache"]

class Disguises(object):
    def __init__(self, world):
        self._world = world
        self._disguises = list()
        self._batch = pyglet.graphics.Batch()
        self.MakeDisguises()
    
    def MakeDisguises(self):
        cellsize = 64
        xlim, ylim = self._world.GridSize()
        for disguise in disguises:
            x, y = (0,0)
            while not self._world.IsPoop(x,y):
                x,y = (cellsize*random.randint(0,xlim-1),
                       cellsize*random.randint(0,ylim-1))
            self._disguises.append(Disguise(disguise, x, y, self._batch))
            
    def Disguises(self):
        return self._disguises
    
    def Remove(self, disguise):
        self._disguises.remove(disguise)
    
    def Draw(self):
        self._batch.draw()

class Disguise(object):
    '''
    classdocs
    '''


    def __init__(self, name, x, y, batch):
        '''
        Constructor
        '''
        self._batch = batch
        pyglet.resource.path = ['data']
        pyglet.resource.reindex()
        o = ordering[name]
        self._sprite = zsprite.ZSprite(pyglet.resource.image("disguise_"+name+".png"),x,y,z=20+o,
                                            batch=self._batch,
                                            subpixel=True)
    
    def Sprite(self):
        return self._sprite
    
    def Collide(self, x, y):
        sx = self._sprite.x
        sy = self._sprite.y
        sw = self._sprite.width
        sh = self._sprite.height
        if x >= sx and x <= sx+sw and y >= sy and y <= sy+sh:
            return True
        return False  
        