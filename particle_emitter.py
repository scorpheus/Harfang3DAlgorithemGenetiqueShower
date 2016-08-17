import gs

import random

plus = gs.GetPlus()

particle_count = 240
particle_spawn_rate = 60 # per second
particles = []
# update particles life and spawn dead particles
spawn_rate_control = 0


def create_particle(scn, nb):
	global particles, particle_count
	particle_count = nb
	particles = []
	# particles don't collide to each other
	scn.GetPhysicSystem().SetCollisionLayerPairState(1, 1, False)
	scn.GetPhysicSystem().SetCollisionLayerPairState(0, 1, True)

	for i in range(particle_count):
		node, rigid_body = gs.GetPlus().AddPhysicSphere(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, -100, 0)), 0.025)
		# avoid the particle to collide to each other
		rigid_body.SetCollisionLayer(1)
		particles.append([0, rigid_body])
		plus.UpdateScene(scn, gs.time(1.0/60))


# update particles life and spawn dead particles
def update_particles(dt_sec, start_pos, direction):
	global particle_spawn_rate, spawn_rate_control
	# update particles and get the dead one
	spawn_rate_control -= dt_sec
	for particle in particles:
		if particle[0] > 0:
			particle[0] -= dt_sec # update life
		elif spawn_rate_control < 0:
			spawn_rate_control += 1.0 / particle_spawn_rate
			particle[0] = particle_count / particle_spawn_rate

			# when teleport the particle rigid body to its spawn position, wake up the rigidbody and reset its world matrix
			rigid_body = particle[1]
			rigid_body.SetIsSleeping(False)
			rigid_body.ResetWorld(gs.Matrix4.TransformationMatrix(start_pos, gs.Vector3(random.random(), random.random(), random.random())))
			rigid_body.ApplyLinearImpulse(direction + gs.Vector3(random.random()*0.1, random.random()*0.1, random.random()*0.1))


def deactivate_all_particles():
	global spawn_rate_control
	spawn_rate_control = 0
	for particle in particles:
		particle[0] = 0
		rigid_body = particle[1]
		rigid_body.ResetWorld(gs.Matrix4.TranslationMatrix(gs.Vector3(-100, -100, -100)))