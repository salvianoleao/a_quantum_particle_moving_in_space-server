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
if "n" not in form or "L" not in form:
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
	L = float(form["L"].value)

	# Generating the probability density graph
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	x = np.linspace(0, L, 900)
	lim1=np.sqrt(2.0/L) # Maximum value of the wavefunction
	fig, ax = plt.subplots()
	ax.axis([0.0,L,0.0,lim1*lim1*1.1])
	str1=r"$n = "+str(n)+r"$"
	ax.plot(x, psi(x,n,L)*psi(x,n,L), label=str1, linewidth=2.8)
	ax.set_xlabel(r'$L$')
	ax.set_ylabel(r'$|\psi_n|^2(x)$')
	plt.title('Probability Density')

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
