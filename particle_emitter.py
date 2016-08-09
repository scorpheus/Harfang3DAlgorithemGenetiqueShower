import gs
import gs.plus.scene as scene
import gs.plus.clock as clock

life_span_sec = 2
particles = None

def create_particle(scn, nb):
	global particles
	particles = []
	for i in range(nb):
		particles.append({"n": scene.add_physic_cube(scn, width=0.1, height=0.1, depth=0.1)[1], "life": 0})


def update(start_pos, dir):
	clock.update()

	# update particles and get the dead one
	dead_particles = []
	for particle in particles:
		particle["life"] -= clock.get_dt()
		if particle["life"] <= 0:
			dead_particles.append(particle)

	for i in range(int(len(dead_particles) *0.1)):
		dead_particles[i]["life"] = life_span_sec
		rigid_body = dead_particles[i]["n"]
		rigid_body.ResetWorld(gs.Matrix4.TranslationMatrix(start_pos))
		rigid_body.ApplyLinearImpulse(dir)

