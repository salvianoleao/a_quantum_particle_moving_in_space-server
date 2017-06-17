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
if "n" not in form or "m" not in form:
	print("Content-Type: text/html")    # HTML is following
	print()                             # blank line, end of headers
	print("<H1>Error</H1>")
	print("Please fill in the name and addr fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	# Defining the wavefunction
	def psi(x,n,L): return np.sqrt(2.0/L)*np.sin(float(n)*np.pi*x/L)

	n = int(form["n"].value)
	m = int(form["m"].value)

	# Defining the wavefunction
	def psi2D(x,y): return 2.0*np.sin(n*np.pi*x)*np.sin(m*np.pi*y)
	
	# Plotting the colorbar for the density plots
	fig = plt.figure(figsize=(10,3))
	colbar = fig.add_axes([0.05, 0.80, 0.7, 0.10])
	norm = mpl.colors.Normalize(vmin=0., vmax=2.0)
	mpl.colorbar.ColorbarBase(colbar, norm=norm, orientation='horizontal')

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
