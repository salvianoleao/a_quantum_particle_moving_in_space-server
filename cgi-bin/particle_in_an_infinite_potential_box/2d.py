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
	print("Please fill in the required fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	n = int(form["n"].value)
	m = int(form["m"].value)

	# Defining the wavefunction
	def psi2D(x,y): return 2.0*np.sin(n*np.pi*x)*np.sin(m*np.pi*y)

	# Generating the wavefunction graph
	x = np.linspace(0, 1, 100)
	y = np.linspace(0, 1, 100)
	X, Y = np.meshgrid(x, y)
	fig, axes = plt.subplots(1, 1, figsize=(8,8))
	axes.imshow(psi2D(X,Y), origin='lower', extent=[0.0, 1.0, 0.0, 1.0])
	axes.set_title(r'Heat plot of $\Psi_{n,m}(x,y)$ for $n='+str(n)+r'$ and $m='+str(m)+r'$')
	axes.set_ylabel(r'$y/L_y$')
	axes.set_xlabel(r'$x/L_x$')

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
