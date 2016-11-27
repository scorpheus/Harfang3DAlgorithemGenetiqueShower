import gs
import neural_network
from create_surface import *

plus = gs.GetPlus()

ground = None
car = None
car_physic = None
layer_count = [5, 500, 500, 500, 3]
inputs = []
scene = None
scene_simple_graphic = None
score_collision = 0
prev_pos = gs.Vector3(0, 0, 0)


def get_name():
	return "car"


def get_gen_count():
	count = 0
	for id, c in enumerate(layer_count):
		if id < len(layer_count) - 1:
			count += layer_count[id] * layer_count[id+1]
	return count


def get_duration_test():
	return 8.0


def initialize_environment(scn):
	global car, car_physic, ground, scene, scene_simple_graphic
	scene = scn
	scn.GetPhysicSystem().SetTimestep(1.0/120)

	scene_simple_graphic = gs.SimpleGraphicSceneOverlay(False)
	scene.AddComponent(scene_simple_graphic)

	ground = plus.AddPhysicPlane(scn)[0]

	car, car_physic = plus.AddPhysicCube(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 0.5, 0)), 0.5, 1, 1, 10)

	# add walls
	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(0, 0, -1.1), gs.Vector3(0, 0, 0)), 4, 3, 1, 0)

	plus.AddPhysicCube(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(-2, 0, 2)), 1, 3, 5, 0)
	plus.AddPhysicCube(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(2, 0, 2)), 1, 3, 5, 0)

	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(-1, 0, 6), gs.Vector3(0, 0.7, 0)), 1, 3, 4, 0)
	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(3, 0, 6), gs.Vector3(0, 0.7, 0)), 1, 3, 4, 0)

	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(1, 0, 8), gs.Vector3(0, 0.7, 0)), 1, 3, 4, 0)
	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(5, 0, 8), gs.Vector3(0, 0.7, 0)), 1, 3, 4, 0)

	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(1, 0, 10), gs.Vector3(0, -0.7, 0)), 1, 3, 4, 0)
	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(5, 0, 10), gs.Vector3(0, -0.7, 0)), 1, 3, 4, 0)

	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(-1, 0, 12), gs.Vector3(0, -0.7, 0)), 1, 3, 4, 0)
	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(3, 0, 12), gs.Vector3(0, -0.7, 0)), 1, 3, 4, 0)
	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(-2, 0, 14), gs.Vector3(0, -0.7, 0)), 1, 3, 4, 0)
	plus.AddPhysicCube(scn, gs.Matrix4.TransformationMatrix(gs.Vector3(1, 0, 14), gs.Vector3(0, -0.7, 0)), 1, 3, 4, 0)


def initiate_test_subject(scn, array_gen):
	global score_collision
	score_collision = 0
	car_physic.SetIsSleeping(False)
	car_physic.ResetWorld(gs.Matrix4.TranslationMatrix(gs.Vector3(0, 0.5, 0)))


def draw_cross(pos):
	size = 0.5
	scene_simple_graphic.Line(pos.x-size, pos.y, pos.z,
	                          pos.x+size, pos.y, pos.z,
	                          gs.Color.Red, gs.Color.Red)
	scene_simple_graphic.Line(pos.x, pos.y-size, pos.z,
	                          pos.x, pos.y+size, pos.z,
	                          gs.Color.Red, gs.Color.Red)
	scene_simple_graphic.Line(pos.x, pos.y, pos.z-size,
	                          pos.x, pos.y, pos.z+size,
	                          gs.Color.Red, gs.Color.Red)


def update(dt_sec, array_gen):
	global inputs

	length_ray = 10
	inputs = []
	# get input
	pos = car.GetTransform().GetPosition()
	pos.y += 0.5
	front_vec = car.GetTransform().GetWorld().GetZ() * 0.51
	pos += front_vec

	angles = [-1.57/3*2, -1.57/3, 0, 1.57/3*2, 1.57/3]

	for id, angle in enumerate(angles):
		rotate_front = (gs.Matrix3.RotationMatrixYAxis(angle) * front_vec).Normalized()
		has_hit, hit = scene.GetSystem("Physic").Raycast(pos, rotate_front, 255, length_ray)
		if has_hit:
			length = gs.Vector3.Dist(pos, hit.GetPosition())
			inputs.append(length / length_ray)
			scene_simple_graphic.Line(pos.x, pos.y, pos.z, pos.x + rotate_front.x * length, pos.y + rotate_front.y * length, pos.z + rotate_front.z * length, gs.Color.White, gs.Color.White)
			draw_cross(hit.GetPosition())
			draw_cross(pos)
		else:
			inputs.append(1)
			scene_simple_graphic.Line(pos.x, pos.y, pos.z, pos.x + rotate_front.x * length_ray, pos.y + rotate_front.y * length_ray, pos.z + rotate_front.z * length_ray, gs.Color.White, gs.Color.White)

	outputs = neural_network.compute_output(inputs, layer_count, array_gen)

	# rotate
	rotate_impulse = outputs[0] * 2 - 1.0
	power_impulse = (outputs[1] * 2 - 1) * 1.5
	# print(rotate_impulse)

	vec_impulse = gs.Matrix3.RotationMatrixYAxis(rotate_impulse) * front_vec * power_impulse
	scene_simple_graphic.Line(pos.x, pos.y, pos.z, pos.x + vec_impulse.x, pos.y + vec_impulse.y, pos.z + vec_impulse.z, gs.Color.Green, gs.Color.Green)

	car_physic.ApplyLinearImpulse(gs.Matrix3.RotationMatrixYAxis(rotate_impulse) * front_vec * power_impulse)


def evaluate_score(scn, current_score):
	global score_collision, prev_pos
	# look if the car collide, and if it's not with the ground
	if scn.GetPhysicSystem().HasCollided(car):
		for pair in scn.GetPhysicSystem().GetCollisionPairs(car):
			if ground != pair.GetNodeA() and ground != pair.GetNodeB():
				score_collision -= 1

	# make bad point if the input is low
	for input in inputs:
		if input < 0.3:
			score_collision -= 1

	if gs.Vector3.Dist2(prev_pos, car.GetTransform().GetPosition()) < 0.01:
		score_collision -= 1

	current_score = score_collision
	current_score += gs.Vector3.Dist(car.GetTransform().GetPosition(), gs.Vector3(0, 0.5, 0)) * 200.0
	return current_score
