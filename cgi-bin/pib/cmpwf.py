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
	# Defining a function to compute the energy
	def En(n,L): return 37.60597*((float(n)/L)**2)
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

	nmax = int(form["n"].value)
	L = float(form["L"].value)
	x = np.linspace(0, L, 900)

	# Generating the wavefunction graph
	fig, ax = plt.subplots(figsize=(12,9))
	ax.spines['right'].set_color('none')
	ax.xaxis.tick_bottom()
	ax.spines['left'].set_color('none')
	ax.axes.get_yaxis().set_visible(False)
	ax.spines['top'].set_color('none')
	X3 = np.linspace(0.0, L, 900,endpoint=True)
	Emax = En(nmax,L)
	amp = (En(2,L)-En(1,L)) *0.9
	Etop = (Emax+amp)*1.1
	ax.axis([-0.5*L,1.5*L,0.0,Etop])
	ax.set_xlabel(r'$X$ (Angstroms)')
	for n in range(1,nmax+1):
		ax.hlines(En(n,L), 0.0, L, linewidth=1.8, linestyle='--', color="black")
		str1="$n = "+str(n)+r"$, $E_{"+str(n)+r"} = %.3f$ eV"%(En(n,L))
		ax.text(1.03*L, En(n,L), str1, fontsize=16, color="black")
		ax.plot(X3,En(n,L)+amp*np.sqrt(L/2.0)*psi(X3,n,L), color="red", label="", linewidth=2.8)
	ax.margins(0.00)
	ax.vlines(0.0, 0.0, Etop, linewidth=4.8, color="blue")
	ax.vlines(L, 0.0, Etop, linewidth=4.8, color="blue")
	ax.hlines(0.0, 0.0, L, linewidth=4.8, color="blue")
	plt.title('Wavefunctions', fontsize=30)
	plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.)
	str2="$V = +\infty$"
	ax.text(-0.15*L, 0.6*Emax, str2, rotation='vertical', fontsize=40, color="black")

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
