import pyglet 
import camera
from pyglet.gl import *
from pyglet.math import Mat4, Vec3
import sys, math
from pyglet import shapes
from snakemodel import Snake
from timecounter import TimeCounter

width  = 1000
height = 1000

window = pyglet.window.Window(width, height, resizable=True)
program = pyglet.graphics.get_default_shader()
snakeBatch = pyglet.graphics.Batch()
counter = TimeCounter(t0=0)

color1 = (0.2, 1.0, 1.0, 1.0)
color2 = (0.4, 1.0, 1.0, 1.0)
newSnake = Snake(color1, color2, batch = snakeBatch)

@window.event
def on_resize(width, height):
    camera.resize( window, width, height )
    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
	window.clear()
	camera.apply(window)
	snakeBatch.draw()
	
@window.event
def on_key_press( key, mods ):	
	if key==pyglet.window.key.Q:
		pyglet.app.exit()
	if key==pyglet.window.key._1:
		print("key 1 pressed")
		
@window.event
def on_mouse_release( x, y, button, mods ):
	global mouseRotatePressed, mouseMovePressed, mouseDollyPressed
	mouseMovePressed   = False
	mouseRotatePressed = False
	mouseDollyPressed   = False

@window.event
def on_mouse_press( x, y, button, mods ):
	global mouseRotatePressed, mouseMovePressed, mouseDollyPressed

	if button & pyglet.window.mouse.LEFT and mods & pyglet.window.key.MOD_SHIFT:
		mouseMovePressed   = True
		mouseRotatePressed = False
		mouseDollyPressed   = False
	elif button & pyglet.window.mouse.LEFT and mods & pyglet.window.key.MOD_CTRL:
		mouseMovePressed   = False
		mouseRotatePressed = False
		mouseDollyPressed   = True
	elif button & pyglet.window.mouse.LEFT:
		camera.beginRotate(x, y)
		mouseMovePressed   = False
		mouseRotatePressed = True
		mouseDollyPressed   = False

@window.event
def on_mouse_drag(x, y, dx, dy, button, mods ):	
	if mouseRotatePressed:
		camera.rotate(x, y)
	elif mouseMovePressed:
		camera.move(dx/width, dy/height, 0.0)
	elif mouseDollyPressed:
		camera.zoom(dy/height)

def update(dt):
	counter.update_time(dt=dt)
	newSnake.set_orientation()



pyglet.clock.schedule_interval(update, 1/60)
glClearColor(0.0, 0.1, 0.3, 1.0)
glEnable(GL_DEPTH_TEST)
glClearDepth(1.0)
glDepthFunc(GL_LESS)

camera.resize( window, width, height )	
pyglet.app.run()