from dana import *
# Population size
n = 4

# Threshold
# -------------------------------------
Cortex_h   =  -3.0
Striatum_h =   0.0
STN_h      = -10.0
GPi_h      =  10.0
Thalamus_h = -40.0

# Time constants
# -------------------------------------
tau = 0.01
Cortex_tau   = tau #0.01#tau #
Striatum_tau = tau #0.01
STN_tau      = tau #0.01
GPi_tau      = tau #0.01
Thalamus_tau = tau #0.01
# Noise leve (%)
# -------------------------------------
if 0:
	Cortex_N   =   0.01
	Striatum_N =   0.001
	STN_N      =   0.001
	GPi_N      =   0.03
	Thalamus_N =   0.001
if 1:
	Cortex_N   =   0.03
	Striatum_N =   0.001
	STN_N      =   0.001
	GPi_N      =   0.001
	Thalamus_N =   0.001


# Populations
# -----------------------------------------------------------------------------
def populations():
	Cortex_cog   = zeros((n,1), """dV/dt = (-V + I + Iext - Cortex_h)/(Cortex_tau);
							   U = noise(V,Cortex_N); I; Iext""")#min_max(V,-3.,60.)
	Cortex_mot   = zeros((1,n), """dV/dt = (-V + I + Iext - Cortex_h)/(Cortex_tau);
							   U = noise(V,Cortex_N); I; Iext""")
	Cortex_ass   = zeros((n,n), """dV/dt = (-V + I + Iext - Cortex_h)/(Cortex_tau);
							   U = noise(V,Cortex_N); I; Iext""")
	Striatum_cog = zeros((n,1), """dV/dt = (-V + I - Striatum_h)/(Striatum_tau);
							   U = noise(sigmoid(V), Striatum_N); I""")
	Striatum_mot = zeros((1,n), """dV/dt = (-V + I - Striatum_h)/(Striatum_tau);
							   U = noise(sigmoid(V), Striatum_N); I""")
	Striatum_ass = zeros((n,n), """dV/dt = (-V + I - Striatum_h)/(Striatum_tau);
							   U = noise(sigmoid(V), Striatum_N); I""")
	STN_cog      = zeros((n,1), """dV/dt = (-V + I - STN_h)/(STN_tau);
							   U = noise(V,STN_N); I""")
	STN_mot      = zeros((1,n), """dV/dt = (-V + I - STN_h)/(STN_tau);
							   U = noise(V,STN_N); I""")
	GPi_cog      = zeros((n,1), """dV/dt = (-V + I - GPi_h)/(GPi_tau);
							   U = noise(V,GPi_N); I""")
	GPi_mot      = zeros((1,n), """dV/dt = (-V + I - GPi_h)/(GPi_tau);
							   U = noise(V,GPi_N); I""")
	Thalamus_cog = zeros((n,1), """dV/dt = (-V + I - Thalamus_h)/(Thalamus_tau);
							   U = noise(V,Thalamus_N); I""")
	Thalamus_mot = zeros((1,n), """dV/dt = (-V + I - Thalamus_h)/(Thalamus_tau);
							   U = noise(V, Thalamus_N); I""")

	return Cortex_cog, Cortex_mot, Cortex_ass, Striatum_cog, Striatum_mot, Striatum_ass, STN_cog, STN_mot, GPi_cog, GPi_mot, Thalamus_cog, Thalamus_mot


