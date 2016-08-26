import gs
import particle_emitter
from create_surface import *
import random
import numpy as np

plus = gs.GetPlus()

surface = None
score_plane = None
width = 50
height = 50
depth = 10

counter_initiate = 0

iso_surface = gs.IsoSurface()


def get_name():
	return "shower_iso"


def get_gen_count():
	return width * height


def get_duration_test():
	return 4.0


# create the plane to evaluate score
def initialize_environment(scn):
	global score_plane
	scn.GetPhysicSystem().SetTimestep(1.0/120)

	plus.AddPhysicPlane(scn)

	# create the plane to evaluate score
	score_plane, rb_plane = plus.AddPhysicPlane(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(2, 1, -1), gs.Vector3(0.75, 0, 0)), 1, 1)

	while score_plane.GetComponent("BoxCollision") is None:
		plus.UpdateScene(scn, gs.time(1.0/60))
	score_plane.GetComponent("BoxCollision").SetDimensions(gs.Vector3(1, 0.1, 1))
	score_plane.GetComponent("BoxCollision").SetMatrix(gs.Matrix4.TranslationMatrix(gs.Vector3(0, -0.05, 0)))

	# initialize particles
	particle_emitter.create_particle(scn, 200)


def add_physic_geo(scn, geo, core_geo, mat=gs.Matrix4.Identity, mass=0, material_path=None):
	"""Create a new plane node, configure its physic attributes, and add it to a scene"""
	node = plus.AddObject(scn, geo, mat)

	rigid_body = gs.MakeRigidBody()
	node.AddComponent(rigid_body)

	collision = gs.MakeMeshCollision()
	collision.SetGeometry(core_geo)
	collision.SetMass(mass)
	node.AddComponent(collision)

	return node, rigid_body


def initiate_test_subject(scn, array_gen):
	global surface, counter_initiate
	particle_emitter.deactivate_all_particles()
	# remove the geometry and add the new one to test
	if surface is not None:
		scn.RemoveNode(surface)

	array = np.zeros((width, depth, height))
	array[:, depth-1, :] = array_gen.reshape((width, height)) * 10

	for i in range(depth - 2, 0, -1):
		array[:, i, :] = array[:, i+1, :]*0.1

	blob = gs.BinaryBlob()
	blob.Grow(array.size)
	blob.WriteFloats(array.flatten().tolist())

	iso_surface.Clear(False)
	gs.PolygoniseIsoSurface(width, height, depth, blob, 0.1, iso_surface, gs.Vector3(0.01, 0.01, 0.1))
	core_geo = gs.CoreGeometry()
	gs.IsoSurfaceToCoreGeometry(iso_surface, core_geo)

	surface, core_surface = add_physic_geo(scn, gs.GetPlus().CreateGeometry(core_geo, False), core_geo, gs.Matrix4.TranslationMatrix((1.8, 2.25, 0.0)))
	counter_initiate += 1
	random.seed(4)


def update(dt_sec, array_gen):
	particle_emitter.update_particles(dt_sec, gs.Vector3(2.5, 3, -1), gs.Vector3(-1, 2, 3))


def evaluate_score(scn, current_score):
	if scn.GetPhysicSystem().HasCollided(score_plane):
		current_score += len(scn.GetPhysicSystem().GetCollisionPairs(score_plane))
	return current_score
