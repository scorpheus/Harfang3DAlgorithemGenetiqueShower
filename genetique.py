import numpy as np
import random
import os

current_generation = 0
nb_test_subject = 50
test_subjects = []


def create_initial_test_subject(name, gen_count):
	global test_subjects
	if os.path.exists("generations_saved_"+name+".npz"):
		npzfile = np.load("generations_saved_"+name+".npz")
		for i in range(len(npzfile.files)):
			test_subjects.append({"a": npzfile[str(i)], "score": 0})

		if len(test_subjects) < nb_test_subject:
			for i in range(nb_test_subject - len(test_subjects)):
				# test_subjects.append({"a": np.random.rand(width * height), "score": 0})
				array = np.empty(gen_count)
				array.fill(0.5)
				test_subjects.append({"a": array, "score": 0})

	else:
		for i in range(nb_test_subject):
			# test_subjects.append({"a": np.random.rand(width * height), "score": 0})
			array = np.empty(gen_count)
			array.fill(0.5)
			test_subjects.append({"a": array, "score": 0})


def save_best_subject(old_best_score, name):
	sorted_subjects = sorted(test_subjects, key=lambda k: k['score'])[::-1]
	if sorted_subjects[0]["score"] > old_best_score:
		np.savez("generations_saved_"+name+"_best", **{"0": sorted_subjects[0]["a"]})


def load_best(name):
	if os.path.exists("generations_saved_"+name+"_best.npz"):
		npzfile = np.load("generations_saved_"+name+"_best.npz")
		return npzfile["0"]
	return None


def make_new_generation(name):
	global test_subjects

	nb_best_subject = 10

	random.seed(current_generation)

	sorted_subjects = sorted(test_subjects, key=lambda k: k['score'])[::-1]

	# save the generation
	generation_to_save = {str(i): v["a"] for i, v in enumerate(sorted_subjects)}
	np.savez("generations_saved_"+name, **generation_to_save)

	# create next generations
	test_subjects = []

	# keep the best subject
	# for i in range(nb_best_subject):
	# 	test_subjects.append({"a": sorted_subjects[i]["a"], "score": 0})

	for i in range(nb_test_subject):
		random.seed(current_generation * nb_test_subject + i )
		array = np.empty(sorted_subjects[0]["a"].shape)
		array.fill(0.5)
		for j in range(array.shape[0]):
			rand = random.random()
			# .001% mutation
			if rand < 0.002:
				rand2 = random.random()
				id_parent = int(rand2 * nb_best_subject)
				# mutate a bit from the parent
				array[j] += (random.random()-0.5) *0.05
			# .01% mutation
			elif rand < 0.02:
				rand2 = random.random()
				id_parent = int(rand2 * nb_best_subject)
				# mutate a bit from the parent
				array[j] = sorted_subjects[id_parent]["a"][j] + (random.random()-0.5) *0.05
			# .01% invert
			elif rand < 0.04:
				rand2 = random.random()
				id_parent = int(rand2 * nb_best_subject)
				rand3 = int(random.random() * array.shape[0])

				# mutate a bit from the parent
				array[j] = sorted_subjects[id_parent]["a"][rand3]
			# mix from the 2 parent
			else:
				rand2 = random.random()
				id_parent = int(rand2 * nb_best_subject)
				# copy the parent gene
				array[j] = sorted_subjects[id_parent]["a"][j]

		test_subjects.append({"a": array, "score": 0})

	return sorted_subjects[0]["score"]