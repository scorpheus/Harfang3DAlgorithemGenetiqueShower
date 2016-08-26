import random
from create_surface import *
import genetique
# import test_cube_launch as experiment
import test_shower as experiment
# import test_shower_iso as experiment

gs.LoadPlugins()

plus = gs.GetPlus()
plus.CreateWorkers()

plus.RenderInit(1024, 768)

plus.GetRendererAsync().SetVSync(False)

scn = plus.NewScene()
# scn.GetPhysicSystem().SetDebugVisuals(True)

cam = plus.AddCamera(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(0, 1, -10)))
plus.AddLight(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(6, 4, -6)))
plus.AddLight(scn, gs.Matrix4.TranslationMatrix(gs.Vector3(-8, 4, -6)))

# initialize subject
genetique.create_initial_test_subject(experiment.get_name(), experiment.get_gen_count())

# create the plane to evaluate score
experiment.initialize_environment(scn)

fps = gs.FPSController(0, 2, -10)

# parameters
current_index_tested = 0
duration_test = experiment.get_duration_test()
test_timer = duration_test
score = 0.0
fixed_timestep = 1.0/60
best_score = -10000


show_the_best = True
if show_the_best:
	array_gen = genetique.load_best(experiment.get_name())

if not show_the_best or array_gen is None:
	array_gen = genetique.test_subjects[current_index_tested]["a"]

experiment.initiate_test_subject(scn, array_gen)

while not plus.IsAppEnded(plus.EndOnEscapePressed | plus.EndOnDefaultWindowClosed):
	dt_sec = plus.UpdateClock()

	if show_the_best:
		fixed_timestep = dt_sec.to_sec()

	fps.UpdateAndApplyToNode(cam, dt_sec)

	# test
	if not show_the_best:
		# if test timer is under 0, take the next to test
		if test_timer < 0:
			# score = experiment.evaluate_score(scn, score)
			genetique.test_subjects[current_index_tested]["score"] = score

			print("change subject, score {0}, {1} id, {2} test_subjects, best score: {3}".format(score, str(current_index_tested + genetique.nb_test_subject*(genetique.current_generation+1)), genetique.current_generation, best_score))

			# test if need to create a new generation
			current_index_tested += 1
			if current_index_tested >= len(genetique.test_subjects):
				genetique.save_best_subject(best_score, experiment.get_name())
				best_score = genetique.make_new_generation(experiment.get_name())
				genetique.current_generation += 1
				current_index_tested = 0
				continue

			test_timer = duration_test
			score = 0.0
			array_gen = genetique.test_subjects[current_index_tested]["a"]

			experiment.initiate_test_subject(scn, array_gen)
		else:
			# count the number of particle colliding
			test_timer -= fixed_timestep
			score = experiment.evaluate_score(scn, score)
	else:
		if plus.KeyDown(gs.InputDevice.KeyR):
			experiment.initiate_test_subject(scn, array_gen)

	experiment.update(fixed_timestep, array_gen)

	plus.UpdateScene(scn, gs.time(fixed_timestep))
	plus.Text2D(5, 20, "Best score: {0}".format(best_score))
	plus.Text2D(5, 5, "Move around with QSZD, left mouse button to look around")
	plus.Flip()
