import gs

import random

life_span_sec = 2
particles = None


def create_particle(scn, nb):
	global particles
	particles = []
	# particles don't collide to each other
	scn.GetPhysicSystem().SetCollisionLayerPairState(4, 4, False)
	scn.GetPhysicSystem().SetCollisionLayerPairState(0, 4, True)

	for i in range(nb):
		node, rigid_body = gs.GetPlus().AddPhysicCube(scn, gs.Matrix4.Identity, 0.05, 0.05, 0.05)
		# avoid the particle to collide to each other
		rigid_body.SetCollisionLayer(4)
		particles.append({"n": rigid_body, "life": 0})


def update(dt_sec, start_pos, dir):
	# update particles and get the dead one
	spawn_number = 0
	for particle in particles:
		particle["life"] -= dt_sec
		if particle["life"] <= 0 and spawn_number < len(particles)*0.1 and random.random() < 0.01:
			spawn_number += 1
			particle["life"] = life_span_sec
			rigid_body = particle["n"]
			rigid_body.ResetWorld(gs.Matrix4.TransformationMatrix(start_pos, gs.Vector3(random.random(), random.random(), random.random())))
			rigid_body.ApplyLinearImpulse(dir + gs.Vector3(random.random()*0.1, random.random()*0.1, random.random()*0.1))


def deactivate_all_particles():
	for particle in particles:
		particle["life"] = 0
		rigid_body = particle["n"]
		rigid_body.ResetWorld(gs.Matrix4.TranslationMatrix(gs.Vector3(-100, -100, -100)))