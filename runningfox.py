import pyglet 
import camera
from pyglet.gl import *
import math
from snakemodel import Snake
import utils
import motion

width  = 1000
height = 1000

window = pyglet.window.Window(width, height, resizable=True, caption="Snake crawls and attacks")


program = pyglet.graphics.get_default_shader()
snakeBatch = pyglet.graphics.Batch()
tailcounter = utils.TimeCounter(t0=0)
liftcounter = utils.TimeCounter(t0=0)
lowercounter = utils.TimeCounter(t0=0)
attackcounter = utils.TimeCounter(t0=0)
event = utils.EventWatcher()

color1 = (0.2, 1.0, 1.0, 1.0)
color2 = (1.0, 1.0, 0.2, 1.0)
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
	if key==pyglet.window.key._3 and event.raisehead==False and event.headsup==False:
		print("key 3 pressed. Start lifting head")
		liftcounter.reset()
		event.raisehead = True
		event.lowerhead = False
	if key==pyglet.window.key._4 and event.lowerhead==False and event.headsup==True:
		print("key 4 pressed. Start lowering head")
		lowercounter.reset()
		event.lowerhead = True
		event.raisehead = False
	if key == pyglet.window.key._1 and event.wavetail==False:
		print("key 1 pressed. Start waving tail")
		tailcounter.reset()
		event.wavetail = True
	if key==pyglet.window.key._2 and event.wavetail==True:
		print("key 2 pressed. Undo waving tail")
		event.wavetail = False
	if key==pyglet.window.key._5 and event.attack==False:
		if event.headsup==True and event.lowerhead==False:
			print("key 5 pressed. Start attack")
			attackcounter.reset()
			event.attack = True
		else:
			print("To attack, first lift the head up by pressing key 3")
	
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

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    camera.zoom(z=-scroll_y*0.1)  # Use scroll_y for zooming


def update(dt):
	orientation = motion.rest_angles
	wave_orient = motion.null_angles

	if event.wavetail==True:
		tailcounter.update_time(dt=dt)
		wave_orient = motion.sinwaveSnake(current_t=tailcounter.t, height=0.3, phase=0, width=math.pi/4, frequency=5)
		orientation = motion.superposition(wave_orient, orientation)

	if event.raisehead==True:
		liftcounter.update_time(dt=dt)
		end_t1 = 1
		lift_orient = motion.raisehead(start_angles=motion.rest_angles, current_t=liftcounter.t, start_t=0, end_t=end_t1)
		if liftcounter.t > end_t1:
			event.headsup = True
		orientation = motion.superposition(wave_orient, lift_orient)

	if event.lowerhead==True and event.headsup==True:
		lowercounter.update_time(dt=dt)
		end_t2 = 1
		lower_orient = motion.lowerhead(start_angles=motion.raisehead_angles, current_t=lowercounter.t, start_t=0, end_t=end_t2)
		if lowercounter.t > end_t2:
			event.headsup=False
		orientation = motion.superposition(wave_orient, lower_orient)
	
	if event.attack==True and event.headsup==True:
		attackcounter.update_time(dt=dt)
		end_t3=1
		attack_orient = motion.attack(start_angles=motion.raisehead_angles, current_t=attackcounter.t, start_t=0, end_t=end_t3)
		if attackcounter.t > end_t3:
			event.attack=False
			event.headsup=True
		orientation = motion.superposition(wave_orient, attack_orient)


	newSnake.set_orientation(orientation)



pyglet.clock.schedule_interval(update, 1/60)
glClearColor(0.0, 0.1, 0.3, 1.0)
glEnable(GL_DEPTH_TEST)
glClearDepth(1.0)
glDepthFunc(GL_LESS)

camera.resize( window, width, height )	
pyglet.app.run()