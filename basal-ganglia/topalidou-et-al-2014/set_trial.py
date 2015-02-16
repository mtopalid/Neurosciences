import numpy as np

cues_mot = np.array([0,1,2,3])
cues_cog = np.array([0,1,2,3])

def set_trial(Cortex_mot, Cortex_cog, Cortex_ass):

    if 1:
		np.random.shuffle(cues_cog)
		np.random.shuffle(cues_mot)
		c1,c2 = cues_cog[:2]
		m1,m2 = cues_mot[:2]
    if 0:
		temp = np.array([0,1])
		np.random.shuffle(temp)
		c1, c2 = temp
		np.random.shuffle(temp)
		m1, m2 = temp
    Cortex_mot['Iext'] = 0
    Cortex_cog['Iext'] = 0
    Cortex_ass['Iext'] = 0

    v = 7
    noise = 0.001
    Cortex_mot['Iext'][0,m1]  = v + np.random.normal(0,v*noise)
    Cortex_mot['Iext'][0,m2]  = v + np.random.normal(0,v*noise)
    Cortex_cog['Iext'][c1,0]  = v + np.random.normal(0,v*noise)
    Cortex_cog['Iext'][c2,0]  = v + np.random.normal(0,v*noise)
    Cortex_ass['Iext'][c1,m1] = v + np.random.normal(0,v*noise)
    Cortex_ass['Iext'][c2,m2] = v + np.random.normal(0,v*noise)

    return c1, c2, m1, m2

def reset_trial(Cortex_mot, Cortex_cog, Cortex_ass):

    Cortex_mot['Iext'] = 0
    Cortex_cog['Iext'] = 0
    Cortex_ass['Iext'] = 0
