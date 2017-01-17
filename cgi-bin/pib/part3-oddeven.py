#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import cgi
import cgitb
cgitb.enable()

import matplotlib as mpl # matplotlib library for plotting and visualization
mpl.use('Agg')
import io
import sys
import matplotlib.pylab as plt # matplotlib library for plotting and visualization
import numpy as np #numpy library for numerical manipulation, especially suited for data arrays

form = cgi.FieldStorage()
if "L" not in form or "Vo" not in form:
	print("Content-Type: text/html")    # HTML is following
	print()                             # blank line, end of headers
	print("<H1>Error</H1>")
	print("Please fill in the name and addr fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	# Reading the input variables from the user
	Vo = float(form["Vo"].value)
	L =  float(form["L"].value)

	val = np.sqrt(2.0*9.10938356e-31*1.60217662e-19)*1e-10/(2.0*1.05457180013e-34) # equal to sqrt(2m*1eV)*1A/(2*hbar)

	# Generating the graph
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	fig, axes = plt.subplots(1, 2, figsize=(13,5))
	axes[0].axis([0.0,Vo,0.0,np.sqrt(Vo)*1.8])
	axes[0].set_xlabel(r'$E$ (eV)')
	axes[0].set_ylabel(r'(eV$^{-1}$)')
	axes[0].set_title('Even solution')
	axes[1].axis([0.0,Vo,0.0,np.sqrt(Vo)*1.8])
	axes[1].set_xlabel(r'$E$ (eV)')
	axes[1].set_ylabel(r'')
	axes[1].set_title('Odd solution')
	E = np.linspace(0.0, Vo, 10000)
	num = int(round((L*np.sqrt(Vo)*val-np.pi/2.0)/np.pi))
	# Removing discontinuity points
	for n in range(10000):
	    for m in range(num+2):
	        if abs(E[n]-((2.0*float(m)+1.0)*np.pi/(2.0*L*val))**2)<0.01: E[n] = np.nan
	        if abs(E[n]-(float(m)*np.pi/(L*val))**2)<0.01: E[n] = np.nan
	# Plotting the curves and setting the labels
	axes[0].plot(E, np.sqrt(Vo-E), label=r"$\sqrt{V_o-E}$", color="blue", linewidth=1.8)
	axes[0].plot(E, np.sqrt(E)*np.tan(L*np.sqrt(E)*val), label=r"$\sqrt{E}\tan(\frac{L\sqrt{2mE}}{2\hbar})$", color="red", linewidth=1.8)
	axes[1].plot(E, np.sqrt(Vo-E), label=r"$\sqrt{V_o-E}$", color="blue", linewidth=1.8)
	axes[1].plot(E, -np.sqrt(E)/np.tan(L*np.sqrt(E)*val), label=r"$-\frac{\sqrt{E}}{\tan(\frac{L\sqrt{2mE}}{2\hbar})}$", color="red", linewidth=1.8)
	# Chosing the positions of the legends
	axes[0].legend(bbox_to_anchor=(0.05, -0.2), loc=2, borderaxespad=0.0)
	axes[1].legend(bbox_to_anchor=(0.05, -0.2), loc=2, borderaxespad=0.0)

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
