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
if "k" not in form or "xmax" not in form or "dk" not in form:
	print("Content-Type: text/html")    # HTML is following
	print()                             # blank line, end of headers
	print("<H1>Error</H1>")
	print("Please fill in the required fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	k = float(form["k"].value)
	xmax = float(form["xmax"].value)
	dk = float(form["dk"].value)

	# Defining functions
	def psi_contour(x,dk): return (np.sin(dk*x)/(np.sqrt(np.pi*dk)*x))
	def psi(x,k,dk): return psi_contour(x,dk)*(np.cos(k*x)+np.sin(k*x)*1j)

	lim1 = np.sqrt(dk/np.pi)
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	x = np.linspace(-xmax, xmax, 900)
	str1=r"$k_o  \pm \Delta k$ = "+str(k)+r" $\pm$ "+str(dk)+r" A$^{-1}$"

	# Generating the probability density graph
	fig, ax = plt.subplots()
	ax.axis([-xmax,xmax,0.0,lim1*lim1*1.1]) # Defining the limits to be plot in the graph
	ax.plot(x, (psi(x,k,dk).real)**2+(psi(x,k,dk).imag)**2,label="Probability Density", color="green") # Plotting the probability density
	# Now we define labels, legend, etc
	ax.legend(loc=2);
	ax.set_xlabel(r'$x$ (Angstroms)')
	ax.set_ylabel(r'$\left|\Psi_{\Delta k}(x)\right|^2$')
	plt.title('Probability Density \n for '+str1)
	lgd = plt.legend(bbox_to_anchor=(1.1, 1), loc=2, borderaxespad=0.0)

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
