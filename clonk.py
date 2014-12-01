'''
Created on 24th April 2013

@author: samgeen
'''

import os, sys, pyglet
from pyglet.window import key, event
from pyglet.gl import * # it already has the gl prefix so OK whatevs

import src.Level as Level
import src.Events as Events
import src.MainGame as MainGame
import src.MakeWeeSplash as MakeWeeSplash
import src.EndScreen as EndScreen

DEBUG = True

screenSize = (1024,768)

class GameWindow(pyglet.window.Window):
    # YAY SUBCLASSING, YOU HAVE NO NEGATIVE EFFECTS WHATSOEVER AND ARE NOT A TERRIBLE IDEA
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearDepth(1.0)
       
        # Clock
        self._clock = pyglet.clock.Clock()
    
        # Stop pyglet burning a hole through the Earth's core with your cpu
        pyglet.clock.set_fps_limit(60)
        
        # Splash screen
        maingame = MainGame.MainGame()
        if not DEBUG:
            self._level = MakeWeeSplash.MakeWeeSplash(maingame)
        else:
            self._level = maingame
        self._level.SetupWindow(self)
        self._player = None
        self._scrollpos = (0,0)

        # Fixes bug in sound under Linux
        pyglet.options['audio'] = ('alsa', 'openal', 'silent')
            
    def ChangeLevel(self, nextLevel):
        '''
        Change the current level
        '''
        # Remove the last level's event handler
        self.pop_handlers()
        # Setup the next level
        self._level = nextLevel
        self._level.SetupWindow(self)

    def Player(self):
        '''
        Return the media player object
        '''
        return self._player

    def update(self):
        self.clear()
        
    def on_resize(self, width, height):
        # As suggested by zsprite.py
        # Based on the default with more useful clipping planes
        # NOTE - set clipping planes to +/- 1000 to avoid cutting out clipping
        x, y = self._scrollpos
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(x, x+width, y, y+height, -1000, 1000)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def ScrollBy(self, dx, dy):
        # Scroll view by this amount
        x0, y0 = self._scrollpos
        self._scrollpos = (x0+dx,y0+dy)
        self.on_resize(self.width, self.height)
        
    def ScrollTo(self, x, y):
        # Scroll view to this position
        self._scrollpos = (x,y)
        self.on_resize(self.width, self.height)
    
    def main_loop(self):

        # Start music
        pyglet.resource.path = ['data']
        pyglet.resource.reindex()
        #music = pyglet.resource.media("overture.mp3")
        #player = pyglet.media.Player()
        #player.eos_action=player.EOS_LOOP
        #player.queue(music)
        #player.play()
        #self._player = player

        time = self._clock.time()
        while not self.has_exit:
            self.clear()

            dtime = self._clock.time() - time 
            time += dtime
            
            self.dispatch_events()
            self.update()
            
            self._level.Run(dtime)

            self.flip()
            pyglet.clock.tick()

def Run():
    gWindow = GameWindow(screenSize[0], screenSize[1],caption = 'CLONK')
    gWindow.main_loop()

if __name__ == '__main__':
    Run()