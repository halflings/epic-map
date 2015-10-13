import itertools

import numpy as np
import pyglet
from pyglet.gl import *


class GameWindow(pyglet.window.Window):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)

        # Setting up OpenGL context
        self.setup_opengl()

        # Setting the resource path
        pyglet.resource.path = ['images']
        pyglet.resource.reindex()

        # Setting-up the clock / max FPS / update event
        self.fps = 80.
        pyglet.clock.schedule_interval(self.update, 1.0/self.fps)
        pyglet.clock.set_fps_limit(self.fps)

        # FPS display, for debugging purposes
        self.fps_display = pyglet.clock.ClockDisplay()


    def setup_opengl(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glClearColor(0.2, 0.2, 0.2, 1)

    def center_coords(self, *points):
        offset = np.array([self.width / 2, self.height / 2])
        for point in points:
            yield offset + point

    def draw_line(self, a, b, color):
        a, b = self.center_coords(a, b)
        coords = tuple(itertools.chain(a.astype(int), b.astype(int)))
        color_tuple = tuple(itertools.chain(color, color))
        glLineWidth(1)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2i', coords),
            ('c3B', color_tuple)
        )


    def draw_quad(self, a, b, c, d, color):
        a, b, c, d = self.center_coords(a, b, c, d)
        coords = np.array(tuple(itertools.chain(a, b, c, d))).astype(int)
        color_tuple = tuple(itertools.chain(color, color, color, color))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
            ('v2i', coords),
            ('c3B', color_tuple)
        )


    def draw_map(self):
        pass

    def on_draw(self):
        self.clear()

        self.draw_map()

        self.fps_display.draw()

    def update(self, dt):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

if __name__ == '__main__':
    window = GameWindow(width=800, height=600)
    pyglet.app.run()