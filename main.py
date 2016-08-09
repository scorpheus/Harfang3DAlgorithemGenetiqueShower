import gs
import gs.plus.render as render
import gs.plus.camera as camera
import gs.plus.input as input
import gs.plus.scene as scene
import gs.plus.clock as clock

import particle_emitter
from create_surface import *
import numpy as np

gs.LoadPlugins(gs.get_default_plugins_path())

render.init(1024, 768, "./pkg.core")

scn = scene.new_scene()

cam = scene.add_camera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, -10)))
scene.add_light(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(6, 4, -6)))
scene.add_physic_cube(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 4, 0)))
scene.add_physic_plane(scn)


def add_physic_geo(scn, geo, core_geo, mat=gs.Matrix4.Identity, mass=0, material_path=None):
	"""Create a new plane node, configure its physic attributes, and add it to a scene"""
	node = scene.add_object(scn, geo, mat)

	rigid_body = gs.MakeRigidBody()
	node.AddComponent(rigid_body)

	collision = gs.MakeMeshCollision()
	collision.SetGeometry(core_geo)
	collision.SetMass(mass)
	node.AddComponent(collision)

	return node, rigid_body

# create the random plane
surface, core_surface = create_surface(9, np.random.rand(200, 200))
add_physic_geo(scn, surface, core_surface)

particle_emitter.create_particle(scn, 200)

fps = camera.fps_controller(0, 2, -10)

while not input.key_press(gs.InputDevice.KeyEscape) and render.get_renderer().GetDefaultOutputWindow().IsOpen():
	dt_sec = clock.update()

	fps.update_and_apply_to_node(cam, dt_sec)

	particle_emitter.update(gs.Vector3(1, 1, -1), gs.Vector3(0, 0, 1))
	scene.update_scene(scn, dt_sec)
	render.text2d(5, 5, "Move around with QSZD, left mouse button to look around")
	render.flip()

render.uninit()