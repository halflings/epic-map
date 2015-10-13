import itertools

import numpy as np
from scipy.spatial import Voronoi
import pyglet
from pyglet.gl import *

RELAXATION_ITERATIONS = 2
MAX_FPS = 80
DEFAULT_NUM_POINTS = 250

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

        # Generate the map
        self.number_points = DEFAULT_NUM_POINTS
        self.generate_map()

    def setup_opengl(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glClearColor(0.2, 0.2, 0.2, 1)

    def generate_map(self):
        # Seed points used to generate the map
        self.points = (np.random.rand(self.number_points, 2) * np.array([self.width, self.height])).astype(int)
        self.voronoi = Voronoi(self.points)

        # Relaxing the generate points
        for i in range(RELAXATION_ITERATIONS):
            self.relax_points()

    def relax_points(self):
        for i in range(self.number_points):
            region = self.voronoi.regions[self.voronoi.point_region[i]]
            if any(v == -1 for v in region):
                continue
            centroid = np.mean([self.voronoi.vertices[v] for v in region], axis=0)
            self.points[i] = centroid.astype(int)
        self.voronoi = Voronoi(self.points)

    def draw_line(self, a, b, color):
        coords = tuple(itertools.chain(a.astype(int), b.astype(int)))
        color_tuple = tuple(itertools.chain(color, color))
        glLineWidth(1)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2i', coords),
            ('c3B', color_tuple)
        )

    def draw_quads(self, points, color=(255, 255, 255)):
        coords = tuple(points.astype(int).flat)
        color_tuple = tuple(np.array([color for i in range(len(points))]).flat)
        pyglet.graphics.draw(len(points), pyglet.gl.GL_QUADS,
            ('v2i', coords),
            ('c3B', color_tuple)
        )


    def draw_map(self):
        # Voronoi background
        for i, region in enumerate(self.voronoi.regions):
            if any(v == -1 for v in region):
                continue
            coords = np.array([self.voronoi.vertices[v] for v in region])
            random_color = (255 * np.array([np.sin(i), np.cos(i), np.tan(i)])).astype(int)
            self.draw_quads(coords, random_color)

        # Voronoi centers
        coords = tuple(self.points.flat)
        pyglet.graphics.draw(len(self.points), pyglet.gl.GL_POINTS,
            ('v2i', coords)
        )



    def on_draw(self):
        self.clear()

        self.draw_map()

        self.fps_display.draw()

    def update(self, dt):
        pass


    def on_mouse_press(self, x, y, button, modifiers):
        self.generate_map()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass


if __name__ == '__main__':
    window = GameWindow(width=800, height=600)
    pyglet.app.run()