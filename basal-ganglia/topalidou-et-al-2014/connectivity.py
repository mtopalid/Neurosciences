from dana import *
import numpy as np
from weights import *

# Population size
n = 4

def connections(Cortex_cog, Cortex_mot, Cortex_ass, Striatum_cog, Striatum_mot, Striatum_ass, STN_cog, STN_mot, GPi_cog, GPi_mot, Thalamus_cog, Thalamus_mot, parameter):

	if parameter == "Nico":
		import parameters_Nico as p
	elif parameter == "Meropi":
		import parameters_me as p

	W_str = DenseConnection( Cortex_cog('U'),   Striatum_cog('I'), p.Cx_Str_cog)
	#init_weights(W_str)
	L = DenseConnection( Cortex_mot('U'),   Striatum_mot('I'), p.Cx_Str_mot)
	init_weights(L)
	L = DenseConnection( Cortex_ass('U'),   Striatum_ass('I'), p.Cx_Str_ass)
	init_weights(L)
	L = DenseConnection( Cortex_cog('U'),   Striatum_ass('I'), p.Cx_cog_Str_ass)
	init_weights(L)
	L = DenseConnection( Cortex_mot('U'),   Striatum_ass('I'), p.Cx_mot_Str_ass)
	init_weights(L)

	DenseConnection( Cortex_cog('U'),   STN_cog('I'),       p.Cx_STN_cog )
	DenseConnection( Cortex_mot('U'),   STN_mot('I'),       p.Cx_STN_mot )
	DenseConnection( Striatum_cog('U'), GPi_cog('I'),       p.Str_Gpi_cog)
	DenseConnection( Striatum_mot('U'), GPi_mot('I'),       p.Str_Gpi_mot )
	DenseConnection( Striatum_ass('U'), GPi_cog('I'),       p.Str_ass_Gpi_cog)
	DenseConnection( Striatum_ass('U'), GPi_mot('I'),       p.Str_ass_Gpi_mot)
	DenseConnection( STN_cog('U'),      GPi_cog('I'),       p.STN_Gpi_cog )
	DenseConnection( STN_mot('U'),      GPi_mot('I'),       p.STN_Gpi_mot )
	DenseConnection( Cortex_cog('U'),   Thalamus_cog('I'),  p.Cx_Th_cog )
	DenseConnection( Cortex_mot('U'),   Thalamus_mot('I'),  p.Cx_Th_mot )

	DenseConnection( Cortex_cog('U'), Cortex_cog('I'), p.Cx_cog_cog)
	DenseConnection( Cortex_mot('U'), Cortex_mot('I'), p.Cx_mot_mot)
	DenseConnection( Cortex_ass('U'), Cortex_ass('I'), p.Cx_ass_ass)
	DenseConnection( Cortex_mot('U'), Cortex_ass('I'), p.Cx_mot_ass)
	DenseConnection( Cortex_ass('U'), Cortex_mot('I'), p.Cx_ass_mot)
	DenseConnection( Cortex_ass('U'), Cortex_cog('I'), p.Cx_ass_cog)

	DenseConnection( Thalamus_cog('U'), Cortex_cog('I'),    p.Th_Cx_cog)
	DenseConnection( Thalamus_mot('U'), Cortex_mot('I'),    p.Th_Cx_mot)
	GPic = DenseConnection( GPi_cog('U'),      Thalamus_cog('I'), p.Gpi_Th_cog )
	GPim = DenseConnection( GPi_mot('U'),      Thalamus_mot('I'), p.Gpi_Th_mot )
	W_cx = DenseConnection( Cortex_cog('U'), Cortex_ass('I'), p.Cx_cog_ass)
	W_cx = init_weights(W_cx, Wmin = 1., Wmax = 2.)
