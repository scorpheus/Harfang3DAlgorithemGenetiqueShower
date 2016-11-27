import numpy as np


# sigmoid function
def nonlin(x, deriv=False):
	if deriv == True:
		return x*(1-x)
	return 1/(1+np.exp(-x))


def compute_output(inputs, layer_count, weights):
	# the input has been already initialize
	compute_layer = inputs #weights[0:layer_count[0]]
	prev_iter = 0
	for id, c in enumerate(layer_count):
		if id < len(layer_count) - 1:
			syn0 = weights[prev_iter:prev_iter + c*layer_count[id + 1]].reshape((c, layer_count[id + 1]))
			compute_layer = nonlin(np.dot(compute_layer, syn0))

			prev_iter = c*layer_count[id + 1]

	return compute_layer