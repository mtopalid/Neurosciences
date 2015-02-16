import numpy as np

# Learning parameters
decision_threshold = 40
alpha_c     = 0.05
alpha_LTP  	= 0.002
alpha_LTD  	= 0.001
Wmin, Wmax 	= 0.25, 0.75

def learning(cues_reward, cues_value, Striatum_cog, W_str, W_cx):
	#Striatal Learning
	# Compute reward
	reward = np.random.uniform(0,1) < cues_reward

	# Compute prediction error
	error = reward - cues_value

	# Update cues values
	cues_value[cgchoice] += error* alpha_c

	# Learn
	lrate = alpha_LTP if error > 0 else alpha_LTD

	dw = error * lrate * Striatum_cog['U'][cgchoice][0]

	w = clip(W_str.weights[cgchoice, cgchoice] + dw, Wmin, Wmax)
	W_str.weights[cgchoice,cgchoice] = w


	# Cortical Learning
	y = W_cx.weights[cgchoice*4:(cgchoice + 1) * 4][cgchoice].reshape((1,4)) * Cortex_ass['U'][cgchoice].reshape((1,4))
	dw_Cortex = 0.0001 * np.dot(y, Cortex_ass['U'][cgchoice])
	w = clip(W_cx.weights[cgchoice*4:(cgchoice + 1) * 4][cgchoice] + dw_Cortex, 0.095, 0.105)
	W_cx.weights[cgchoice*4:(cgchoice + 1) * 4][cgchoice] = w

    #W += alpha_LTP * np.minimum(CTX.cog.V,5.0)
