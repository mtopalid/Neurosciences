# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License.
#
# Contributors:
#  * Nicolas P. Rougier (Nicolas.Rougier@inria.fr)
#  * Meropi Topalidou (Meropi.Topalidou@inria.fr)
# -----------------------------------------------------------------------------

# Packages import
import sys
from dana import *
from trial import *
from display import *
from weights import *
from group_functions import *
from populations import *
from connectivity import *
import matplotlib.pyplot as plt
import os

# Simulation parameters
# -----------------------------------------------------------------------------
# Population size
n = 4

# Trial duration
duration = 3.0*second

# Default Time resolution
dt = 1.0*millisecond

Cortex_cog, Cortex_mot, Cortex_ass, Striatum_cog, Striatum_mot, Striatum_ass, STN_cog, STN_mot, GPi_cog, GPi_mot, Thalamus_cog, Thalamus_mot = populations()
connections(Cortex_cog, Cortex_mot, Cortex_ass, Striatum_cog, Striatum_mot, Striatum_ass, STN_cog, STN_mot, GPi_cog, GPi_mot, Thalamus_cog, Thalamus_mot, "Nico")

start = 500*millisecond
# Trial setup
@clock.at(start)
def trial(t):
	global c1, c2, m1, m2
	c1, c2, m1, m2 = set_trial(Cortex_mot, Cortex_cog, Cortex_ass)

@clock.at(2.5*second + start)
def rt_trial(t):
    reset_trial(Cortex_mot, Cortex_cog, Cortex_ass)

size = int(duration/dt)
timesteps   = np.zeros(size)
motor       = np.zeros((5, n, size))
cognitive   = np.zeros((5, n, size))

motch = 0

@after(clock.tick)
def register(t):
    global motch
    ind = int(t*1000)
    timesteps[ind] = t
    motor[0,:,ind] = Cortex_mot['U'].ravel()
    cognitive[0,:,ind] = Cortex_cog['U'].ravel()

    mot_choice = np.argmax(Cortex_mot['U'])

    # Check if Motor took a decision
    if abs(Cortex_mot['U'].max() - Cortex_mot['U'].min()) > 40.0 and motch == 0:

		motch =1
		debug(mot_choice, c1, m1, c2, m2)


# Run simulation
np.random.seed(123)
Guthrie = True
us = False
clock.reset()
reset(network, Cortex_mot, Cortex_cog, Cortex_ass)
run(time=duration, dt=dt)

figure(timesteps, cognitive, motor)
