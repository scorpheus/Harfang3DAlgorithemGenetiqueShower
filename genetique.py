import numpy as np
import random
import os
import gs

current_generation = 0
nb_test_subject = 50
test_subjects = []


def create_initial_test_subject(width, height):
	global test_subjects
	if os.path.exists("generations_saved.npz"):
		npzfile = np.load("generations_saved.npz")
		for i in range(len(npzfile.files)):
			test_subjects.append({"a": npzfile[str(i)], "score": 0})

		if len(test_subjects) < nb_test_subject:
			for i in range(nb_test_subject - len(test_subjects)):
				# test_subjects.append({"a": np.random.rand(width * height), "score": 0})
				array = np.empty(width * height)
				array.fill(0.5)
				test_subjects.append({"a": array, "score": 0})

	else:
		for i in range(nb_test_subject):
			# test_subjects.append({"a": np.random.rand(width * height), "score": 0})
			array = np.empty(width * height)
			array.fill(0.5)
			test_subjects.append({"a": array, "score": 0})


def make_new_generation():
	global test_subjects

	nb_best_subject = 10

	random.seed(current_generation)

	# save the generation
	generation_to_save = {str(i):v["a"] for i, v in enumerate(test_subjects)}
	np.savez("generations_saved", **generation_to_save)

	sorted_subjects = sorted(test_subjects, key=lambda k: k['score'])[::-1]

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
			# # if there is no code, maybe mutate a bit
			# if subject_a[j] == 0.5 or subject_b[j] == 0.5:
			# 	rand = random.random()
			# 	# .001% mutation
			# 	if rand < 0.001:
			# 		array[j] += (random.random()-0.5) *0.05
			# else:
			rand = random.random()
			# .01% mutation
			if rand < 0.001:
				rand2 = random.random()
				id_parent = int(rand2 * nb_best_subject)
				# mutate a bit from the parent
				array[j] = sorted_subjects[id_parent]["a"][j] + (random.random()-0.5) *0.05
			# mix from the 2 parent
			else:
				rand2 = random.random()
				id_parent = int(rand2 * nb_best_subject)
				# copy the parent gene
				array[j] = sorted_subjects[id_parent]["a"][j]

			# # .01% mutation
			# # if rand < 0.001:
			# # 	array[j] = random.random()
			# # 5% from parent A
			# if rand < 0.05:
			# 	array[j] = subject_a[j]
			# # 5% from parent B
			# elif rand < 0.10:
			# 	array[j] = subject_b[j]
			# # 5% from parent A + rand
			# elif rand < 0.15:
			# 	array[j] = subject_a[j] + random.random() *0.01
			# # 5% from parent B + rand
			# elif rand < 0.20:
			# 	array[j] = subject_b[j] + random.random() *0.01
			# # mix from the 2 parent
			# else:
			# 	mix_rand = random.random()
			# 	array[j] = mix_rand * subject_a[j] + (1-mix_rand) * subject_b[j]

		test_subjects.append({"a": array, "score": 0})

	return sorted_subjects[0]["score"]