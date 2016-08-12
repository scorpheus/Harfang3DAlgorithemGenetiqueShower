import gs

import random

plus = gs.GetPlus()

life_span_sec = 2
spawn_rate = 1
particles = None
spawn_every_sec = 1.0/60
spawn_timer = 0


def create_particle(scn, nb):
	global particles
	particles = []
	# particles don't collide to each other
	scn.GetPhysicSystem().SetCollisionLayerPairState(1, 1, False)
	scn.GetPhysicSystem().SetCollisionLayerPairState(0, 1, True)

	for i in range(nb):
		node, rigid_body = gs.GetPlus().AddPhysicSphere(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, -100, 0)), 0.025)
		# avoid the particle to collide to each other
		rigid_body.SetCollisionLayer(1)
		particles.append({"n": rigid_body, "life": 0})
		plus.UpdateScene(scn, gs.time(1.0/60))


def update(dt_sec, start_pos, dir):
	global spawn_timer
	# update particles and get the dead one
	spawn_number = 0
	spawn_timer -= dt_sec
	for particle in particles:
		particle["life"] -= dt_sec
		if spawn_timer <= 0:
			if particle["life"] <= 0 and spawn_number < spawn_rate:
				spawn_number += 1
				particle["life"] = life_span_sec
				rigid_body = particle["n"]
				rigid_body.SetIsSleeping(False)
				rigid_body.ResetWorld(gs.Matrix4.TransformationMatrix(start_pos, gs.Vector3(random.random(), random.random(), random.random())))
				rigid_body.ApplyLinearImpulse(dir + gs.Vector3(random.random()*0.1, random.random()*0.1, random.random()*0.1))

	if spawn_timer <= 0:
		spawn_timer = spawn_every_sec


def deactivate_all_particles():
	for particle in particles:
		particle["life"] = 0
		rigid_body = particle["n"]
		rigid_body.ResetWorld(gs.Matrix4.TranslationMatrix(gs.Vector3(-100, -100, -100)))