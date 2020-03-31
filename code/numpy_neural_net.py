#Big credits: https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795

import numpy as np

def sigmoid(Z):
	return 1/(1+np.exp(-Z))

def relu(Z):
	return np.maximum(0,Z)

def sigmoid_backward(dA, Z):
	sig = sigmoid(Z)
	return dA * sig * (1 - sig)

def relu_backward(dA, Z):
	dZ = np.array(dA, copy=True)
	dZ[Z <= 0] = 0
	return dZ

def convert_prob_into_class(probs):
	probs_ = np.copy(probs)
	probs_[probs_ > 0.5] = 1
	probs_[probs_ <= 0.5] = 0
	return probs_

def get_activation(activation):
	if activation == "relu":
		return relu
	elif activation == "relu_backward":
		return relu_backward
	elif activation == "sigmoid":
		return sigmoid
	elif activation == "sigmoid_backward":
		return sigmoid_backward
	else:
		raise Exception('Non-supported activation function', activation)

def get_cost_value(Y_hat, Y):
	m = Y_hat.shape[1]
	cost = -1 / m * (np.dot(Y, np.log(Y_hat).T) + np.dot(1 - Y, np.log(1 - Y_hat).T))
	return float(np.squeeze(cost))

def get_accuracy_value(Y_hat, Y):
	Y_hat_ = convert_prob_into_class(Y_hat)
	return (Y_hat_ == Y).all(axis=0).mean()

nn_architecture = [
	{"input_dim": 2, "output_dim": 4, "activation": "relu"},
	{"input_dim": 4, "output_dim": 6, "activation": "relu"},
	{"input_dim": 6, "output_dim": 6, "activation": "relu"},
	{"input_dim": 6, "output_dim": 4, "activation": "relu"},
	{"input_dim": 4, "output_dim": 1, "activation": "sigmoid"},
]

def init_layers(nn_architecture, seed=1):
	np.random.seed(seed)
	num_layers = len(nn_architecture)
	params_values = {}

	for idx, layer in enumerate(nn_architecture):
		layer_idx = idx + 1
		layer_input_size = nn_architecture[idx]["input_dim"]
		layer_output_size = nn_architecture[idx]["output_dim"]

		params_values[f"W{layer_idx}"] = np.random.randn(layer_output_size, layer_input_size) * 0.3
		params_values[f"b{layer_idx}"] = np.random.randn(layer_output_size, 1) * 0.3

	return params_values

def forward(A_prev, W_curr, b_curr, activation):

	activation_func = get_activation(activation)
	Z_curr = np.dot(W_curr, A_prev) + b_curr
	A_curr = activation_func(Z_curr)

	return A_curr, Z_curr

def network_forward(X, params_values, nn_architecture):

	memory = {"A0": X}
	A_curr = X

	for idx in range(len(nn_architecture)):
		layer_idx = idx + 1
		A_prev = A_curr
		W_curr = params_values[f"W{layer_idx}"]
		b_curr = params_values[f"b{layer_idx}"]
		activation = nn_architecture[idx]["activation"]

		A_curr, Z_curr = forward(A_prev, W_curr, b_curr, activation)

		memory[f"A{layer_idx}"] = A_curr
		memory[f"Z{layer_idx}"] = Z_curr

	return A_curr, memory

def backprop(dA_curr, W_curr, b_curr, Z_curr, A_prev, activation):
	m = A_prev.shape[1]

	# this will use the chain rule: dZ = dA * g'(Z)
	backward_activation_func = get_activation(activation)

	# how much the outputs should change (dZ_curr) 
	# is the product of
	# (1) how much the activated output should change (dA_curr) 
	# (2) (the derivative of the activation function) applied to Z_curr
	dZ_curr = backward_activation_func(dA_curr, Z_curr)

	# how much the current weights should change (dW_curr)
	# is the product of
	# (1) how much the output should change (dZ_curr) 
	# (2) the input for this layer (A_prev)
	dW_curr = np.dot(dZ_curr, A_prev.T) / m

	db_curr = np.sum(dZ_curr, axis=1, keepdims=True) / m

	# how much the activated outputs from the previous layer should change
	# is the product of 
	# (1) the weights at this layer (W_curr)
	# (2) how much the outputs of this layer should change
	dA_prev = np.dot(W_curr.T, dZ_curr)

	return dA_prev, dW_curr, db_curr

def network_backprop(Y_hat, Y, memory, params_values, nn_architecture):
	grad_values = {}
	m = Y.shape[1]
	Y = Y.reshape(Y_hat.shape)

	dA_prev = - (np.divide(Y, Y_hat)) + np.divide(1 - Y, 1 - Y_hat) # derivative of the cross-entropy loss function

	for layer_idx_prev, layer in reversed(list(enumerate(nn_architecture))):
		layer_idx_curr = layer_idx_prev + 1
		activation_function_curr = str(layer["activation"] + "_backward")

		dA_curr = dA_prev 

		A_prev = memory[f"A{layer_idx_prev}"]
		Z_curr = memory[f"Z{layer_idx_curr}"]
		W_curr = params_values[f"W{layer_idx_curr}"]
		b_curr = params_values[f"b{layer_idx_curr}"]

		dA_prev, dW_curr, db_curr = backprop(dA_curr, W_curr, b_curr, Z_curr, A_prev, activation_function_curr)

		grad_values[f"dW{layer_idx_curr}"] = dW_curr
		grad_values[f"db{layer_idx_curr}"] = db_curr
	
	return grad_values

def update_network(params_values, grad_values, nn_architecture, learning_rate=0.001):
	for i, layer in enumerate(nn_architecture):
		layer_idx = i + 1
		params_values[f"W{layer_idx}"] -= learning_rate * grad_values[f"dW{layer_idx}"]
		params_values[f"b{layer_idx}"] -= learning_rate * grad_values[f"db{layer_idx}"]
	return params_values

def train_network(X, epochs=3000):
	params_values = init_layers(nn_architecture)
	cost_history = []
	acc_history = []

	A_curr, memory = network_forward(X, params_values, nn_architecture)

	for epoch in range(epochs):
		A_curr, memory = network_forward(X, params_values, nn_architecture)
		grad_values = network_backprop(A_curr, Y, memory, params_values, nn_architecture)
		params_values = update_network(params_values, grad_values, nn_architecture)

		if epoch % 100 == 0:
			cost = get_cost_value(A_curr, Y)
			cost_history.append(cost)
			acc = get_accuracy_value(A_curr, Y)
			acc_history.append(acc)
			print(A_curr)

	print(f"cost_history: {cost_history}")
	print(f"acc_history: {acc_history}")

if __name__ == "__main__":
	X = np.random.randn(2, 6) * 100
	Y = np.array([[0, 0, 0, 1, 1, 1]])
	train_network(X)