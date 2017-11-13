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
if "n" not in form or "m" not in form or "yo" not in form or "xo" not in form:
	print("Content-Type: text/html")    # HTML is following
	print()                             # blank line, end of headers
	print("<H1>Error</H1>")
	print("Please fill in the required fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	# Here the users inputs the values of n and m
	n = int(form["n"].value)
	m = int(form["m"].value)
	yo = float(form["yo"].value)
	xo = float(form["xo"].value)

	def psi2D(x,y): return 2.0*np.sin(n*np.pi*x)*np.sin(m*np.pi*y)

	# Generating the wavefunction graph
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	x = np.linspace(0, 1.0, 900)
	fig, ax = plt.subplots()
	lim1=2.0 # Maximum value of the wavefunction
	ax.axis([0.0,1.0,-1.1*lim1,1.1*lim1]) # Defining the limits to be plot in the graph
	str1=r"$n = "+str(n)+r", m = "+str(m)+r", y_o = "+str(yo)+r"\times L_y$"
	ax.plot(x, psi2D(x,yo), linestyle='--', label=str1, color="orange", linewidth=2.8) # Plotting the wavefunction
	ax.hlines(0.0, 0.0, 1.0, linewidth=1.8, linestyle='--', color="black") # Adding a horizontal line at 0
	# Now we define labels, legend, etc
	ax.legend(loc=2);
	ax.set_xlabel(r'$x/L_x$')
	ax.set_ylabel(r'$\sqrt{L_xL_y}\Psi_{n,m}(x,y_o)$')
	lgd = plt.legend(bbox_to_anchor=(1.1, 1), loc=2, borderaxespad=0.0)

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
