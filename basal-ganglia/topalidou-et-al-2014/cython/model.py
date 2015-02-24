# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier
# Distributed under the (new) BSD License.
#
# Contributors: Nicolas P. Rougier (Nicolas.Rougier@inria.fr)
# -----------------------------------------------------------------------------
from c_dana import *
from parameters import *

clamp   = Clamp(min=0, max=1000)
sigmoid = Sigmoid(Vmin=Vmin, Vmax=Vmax, Vh=Vh, Vc=Vc)

CTX = AssociativeStructure(
    tau=tau, rest=CTX_rest, noise=0.03, activation=clamp )
STR = AssociativeStructure(
                 tau=tau, rest=STR_rest, noise=noise, activation=sigmoid )
STN = Structure( tau=tau, rest=STN_rest, noise=noise, activation=clamp )
GPI = Structure( tau=tau, rest=GPI_rest, noise=noise, activation=clamp )
THL = Structure( tau=tau, rest=THL_rest, noise=noise, activation=clamp )
structures = (CTX, STR, STN, GPI, THL)

CUE = np.zeros(4, dtype=[("mot", float),
                         ("cog", float),
                         ("value" , float),
                         ("reward", float)])

choices  = np.array([[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])
cues_cog = choices.copy()
for i in range(1,30):
	cues_cog = np.vstack((cues_cog,choices))
np.random.shuffle(cues_cog)

CUE["mot"]    = 0,1,2,3
CUE["cog"]    = 0,1,2,3
CUE["value"]  = 0.5
CUE["reward"] = rewards

def weights(shape):
    N = np.random.normal(0.5, 0.005, shape)
    N = np.minimum(np.maximum(N, 0.0),1.0)
    return (Wmin+(Wmax-Wmin)*N)

W1 = (2*np.eye(4) - np.ones((4,4))).ravel()
W2 = (2*np.eye(16) - np.ones((16,16))).ravel()

connections = {
    "CTX.cog -> STR.cog" : OneToOne( CTX.cog.V, STR.cog.Isyn, weights(4)  ), # plastic (RL)
    "CTX.mot -> STR.mot" : OneToOne( CTX.mot.V, STR.mot.Isyn, weights(4)  ),
    "CTX.ass -> STR.ass" : OneToOne( CTX.ass.V, STR.ass.Isyn, weights(4*4)),
    "CTX.cog -> STR.ass" : CogToAss( CTX.cog.V, STR.ass.Isyn, weights(4)  ),
    "CTX.mot -> STR.ass" : MotToAss( CTX.mot.V, STR.ass.Isyn, weights(4)  ),
    "CTX.cog -> STN.cog" : OneToOne( CTX.cog.V, STN.cog.Isyn, np.ones(4)  ),
    "CTX.mot -> STN.mot" : OneToOne( CTX.mot.V, STN.mot.Isyn, np.ones(4)  ),
    "STR.cog -> GPI.cog" : OneToOne( STR.cog.V, GPI.cog.Isyn, np.ones(4)  ),
    "STR.mot -> GPI.mot" : OneToOne( STR.mot.V, GPI.mot.Isyn, np.ones(4)  ),
    "STR.ass -> GPI.cog" : AssToCog( STR.ass.V, GPI.cog.Isyn, np.ones(4)  ),
    "STR.ass -> GPI.mot" : AssToMot( STR.ass.V, GPI.mot.Isyn, np.ones(4)  ),
    "STN.cog -> GPI.cog" : OneToAll( STN.cog.V, GPI.cog.Isyn, np.ones(4)  ),
    "STN.mot -> GPI.mot" : OneToAll( STN.mot.V, GPI.mot.Isyn, np.ones(4)  ),
    "THL.cog -> CTX.cog" : OneToOne( THL.cog.V, CTX.cog.Isyn, np.ones(4)  ),  # changed
    "THL.mot -> CTX.mot" : OneToOne( THL.mot.V, CTX.mot.Isyn, np.ones(4)  ),  # changed
    "CTX.cog -> THL.cog" : OneToOne( CTX.cog.V, THL.cog.Isyn, np.ones(4)  ),  # changed
    "CTX.mot -> THL.mot" : OneToOne( CTX.mot.V, THL.mot.Isyn, np.ones(4)  ),  # changed
    "CTX.mot -> CTX.mot" : AllToAll( CTX.mot.V, CTX.mot.Isyn, W1,         ),  # new
    "CTX.cog -> CTX.cog" : AllToAll( CTX.cog.V, CTX.cog.Isyn, W1,         ),  # new
    "CTX.ass -> CTX.ass" : AllToAll( CTX.ass.V, CTX.ass.Isyn, W2,         ),  # new
    "CTX.ass -> CTX.cog" : AssToCog( CTX.ass.V, CTX.cog.Isyn, np.ones(4), ), # new (null ?)
    "CTX.ass -> CTX.mot" : AssToMot( CTX.ass.V, CTX.mot.Isyn, np.ones(4), ), # new
    "CTX.cog -> CTX.ass" : CogToAss( CTX.cog.V, CTX.ass.Isyn, np.ones(4)  ), # plastic (Hebbian)
    "CTX.mot -> CTX.ass" : MotToAss( CTX.mot.V, CTX.ass.Isyn, np.ones(4), ), # new (null ?)
    "GPI.cog -> THL.cog" : OneToOne( GPI.cog.V, THL.cog.Isyn, np.ones(4), ), # changed
    "GPI.mot -> THL.mot" : OneToOne( GPI.mot.V, THL.mot.Isyn, np.ones(4), ), # changed
}
for name,gain in gains.items():
    connections[name].gain = gain



# -----------------------------------------------------------------------------
def set_trial(n=2, cog_shuffle=True, mot_shuffle=True, noise=noise, trial = None):

    if trial is not None:
    	temp = np.array([cues_cog[trial,0], cues_cog[trial,1]])
    	np.random.shuffle(temp)
    	CUE["cog"][0], CUE["cog"][1] = temp
    else:
		if cog_shuffle:
			np.random.shuffle(CUE["cog"])
    if mot_shuffle:
        np.random.shuffle(CUE["mot"])
    CTX.mot.Iext = 0
    CTX.cog.Iext = 0
    CTX.ass.Iext = 0
    for i in range(n):
        c, m = CUE["cog"][i], CUE["mot"][i]
        #CTX.mot.Iext[m]     = V_cue + np.random.normal(0,V_cue*noise)
        #CTX.cog.Iext[c]     = V_cue + np.random.normal(0,V_cue*noise)
        #CTX.ass.Iext[c*4+m] = V_cue + np.random.normal(0,V_cue*noise)

        CTX.mot.Iext[m]     = V_cue + np.random.uniform(-noise/2,noise/2)
        CTX.cog.Iext[c]     = V_cue + np.random.uniform(-noise/2,noise/2)
        CTX.ass.Iext[c*4+m] = V_cue + np.random.uniform(-noise/2,noise/2)


def iterate(dt):
    # Flush connections
    for connection in connections.values():
        connection.flush()

    # Propagate activities
    for connection in connections.values():
        connection.propagate()

    # Compute new activities
    for structure in structures:
        structure.evaluate(dt)


def reset():
    CUE["mot"]    = 0,1,2,3
    CUE["cog"]    = 0,1,2,3
    CUE["value"]  = 0.5
    # CUE["reward"] = rewards
    connections["CTX.cog -> STR.cog"].weights = weights(4)
    connections["CTX.cog -> CTX.ass"].weights = np.ones(4)
    connections["CTX.mot -> CTX.ass"].weights = np.ones(4)
    reset_activities()

def reset_activities():
    for structure in structures:
        structure.reset()


def process(n=2, learning=True):
    # A motor decision has been made
    # The actual cognitive choice may differ from the cognitive choice
    # Only the motor decision can designate the chosen cue
    mot_choice = np.argmax(CTX.mot.V)
    for i in range(n):
        #print mot_choice, CUE["mot"][:n][i]
        if mot_choice == CUE["mot"][:n][i]:
            cog_choice = CUE["cog"][:n][i]
    choice = cog_choice

    # Compute reward
    reward = int(np.random.uniform(0,1) < CUE["reward"][choice])

    # Compute prediction error
    error = reward - CUE["value"][choice]

    # Update cues values
    CUE["value"][choice] += error* alpha_CUE

    if isinstance(learning,(bool,int)):
        learning = learning,learning

    if learning[0]:
        # Reinforcement learning
        lrate = alpha_LTP if error > 0 else alpha_LTD
        dw = error * lrate * STR.cog.U[choice]
        W = connections["CTX.cog -> STR.cog"].weights
        W[choice] = min(max(W[choice]+dw,Wmin),Wmax)

    if learning[1]:
        # Hebbian learning
        W = connections["CTX.cog -> CTX.ass"].weights
        W += alpha_LTP * np.minimum(CTX.cog.V,1.0)
        W = connections["CTX.mot -> CTX.ass"].weights
        W += alpha_LTP * np.minimum(CTX.mot.V,0.5)

    return CUE["cog"][:n], choice, reward

def debug(time, cues, choice, reward):
    n = len(cues)
    cues = np.sort(cues)

    R.append(reward)
    if choice == cues[0]:
        P.append(1)
    else:
        P.append(0)

    print "Choice:         ",
    for i in range(n):
        if choice == cues[i]:
            print "[%d]" % cues[i],
        else:
            print "%d" % cues[i],
        if i < (n-1):
            print "/",
    if choice == cues[0]:
        print " (good)"
    else:
        print " (bad)"

    print "Reward (%3d%%) :   %d" % (int(100*CUE["reward"][choice]),reward)
    print "Mean performance: %.3f" % np.array(P).mean()
    print "Mean reward:      %.3f" % np.array(R).mean()
    print "Response time:    %d ms" % (time)
    print "CTX.cog->CTX.ass:", connections["CTX.cog -> CTX.ass"].weights
    print
