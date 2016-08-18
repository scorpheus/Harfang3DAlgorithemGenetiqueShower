import gs
import random

plus = gs.GetPlus()

cube = None
rb_cube = None


def get_name():
	return "cube_launch"


def get_gen_count():
	return 3


def get_duration_test():
	return 20.0


# create the plane to evaluate score
def initialize_environment(scn):
	global cube, rb_cube
	plus.AddPhysicPlane(scn)
	plus.AddSphere(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(10, 1, 0)), 1)
	plus.AddSphere(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, 0)), 1)
	cube, rb_cube = plus.AddPhysicSphere(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, 0)), 1)


def initiate_test_subject(scn, array_gen):
	rb_cube.SetIsSleeping(False)
	rb_cube.ResetWorld(gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, 0)))
	rb_cube.ApplyLinearImpulse(gs.Vector3(array_gen[0], array_gen[1], array_gen[2])*10)

	random.seed(4)


def update(dt_sec, array_gen):
	pass


def evaluate_score(scn, current_score):
	return gs.Vector3.Dist(gs.Vector3(10, 1, 0), cube.GetTransform().GetPosition()) * -1.0
