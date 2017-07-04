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
if "k" not in form or "xmax" not in form:
	print("Content-Type: text/html")    # HTML is following
	print()                             # blank line, end of headers
	print("<H1>Error</H1>")
	print("Please fill in the required fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	k = float(form["k"].value)
	xmax = float(form["xmax"].value)

	# Defining Psi and PsiC (complex conjugate) functions
	def psi(x,k): return (1.0/np.sqrt(2.0*np.pi))*(np.cos(k*x)+np.sin(k*x)*1j)
	def psiC(x,k): return (1.0/np.sqrt(2.0*np.pi))*(np.cos(k*x)-np.sin(k*x)*1j)

	# Generating the wavefunction graph
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	x = np.linspace(-xmax, xmax, 900)
	fig, ax = plt.subplots()
	lim1=1/np.sqrt(2*np.pi) # Maximum value of the wavefunction
	ax.axis([-xmax,xmax,-lim1*1.1,lim1*1.1]) # Defining the limits to be plot in the graph
	ax.plot(x, psi(x,k).real, label="Real", color="blue") # Ploting the real part of the wavefunction
	ax.plot(x, psi(x,k).imag, label="Imag.", color="red") # Ploting the real part of the wavefunction
	ax.hlines(0.0, -xmax, xmax, linewidth=1.8, linestyle='--', color="black") # Adding a horizontal line at 0
	# Now we define labels, legend, etc
	ax.legend(loc=2);
	ax.set_xlabel(r'$x$ (Angstroms)')
	ax.set_ylabel(r'$\psi_k(x)$')
	str1=r"$k$ = "+str(k)+r" A$^{-1}$"
	plt.title('Wavefunction for '+str1)
	lgd = plt.legend(bbox_to_anchor=(1.1, 1), loc=2, borderaxespad=0.0)

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
