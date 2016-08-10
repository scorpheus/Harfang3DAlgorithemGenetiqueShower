import numpy as np
import random

current_generation = 0
nb_test_subject = 5
test_subjects = []

for i in range(nb_test_subject):
	# test_subjects.append({"a": np.random.rand(200 * 200), "score": 0})
	test_subjects.append({"a": np.zeros(200 * 200), "score": 0})


def make_new_generation():
	global test_subjects
	sorted_subjects = sorted(test_subjects, key=lambda k: k['score'])[::-1]

	# get the 2 most scored subject
	subject_a = sorted_subjects[0]["a"]
	subject_b = sorted_subjects[0]["a"]

	# create next generations
	test_subjects = []

	for i in range(nb_test_subject):
		array = np.zeros((200 * 200))
		for j in range(array.shape[0]):
			rand = random.random()
			# 1% mutation
			if rand < 0.01:
				array[j] = random.random()
			# 10% from parent A
			elif rand < 0.11:
				array[j] = subject_a[j]
			# 10% from parent B
			elif rand < 0.21:
				array[j] = subject_b[j]
			# mix from the 2 parent
			else:
				mix_rand = random.random()
				array[j] = mix_rand * subject_a[j] + (1-mix_rand) * subject_b[j]

		test_subjects.append({"a": array, "score": 0})
