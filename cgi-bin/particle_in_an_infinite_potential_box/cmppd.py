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
	print("Please fill in the required fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	nmax = int(form["n"].value)
	L = float(form["L"].value)

	# Defining the wavefunction
	def psi(x,n,L): return np.sqrt(2.0/L)*np.sin(float(n)*np.pi*x/L)
	#Given the following parameters
	h=6.62607e-34    #planck's constant in joules
	me=9.1093837e-31  # mass of an electron in kg
	# (h**2 / (me*8))* (1e10)**2 *6.242e+18  #is the prefactor using length units is Angstroms and then converted into electron volts
	# Defining a function to compute the energy
	def En(n,L,m): return (h**2 / (m*8))* (1e10)**2 *6.242e+18*((float(n)/L)**2)
	Emax = En(nmax,L,me)
	amp = (En(2,L,me)-En(1,L,me)) *0.9
	Etop = (Emax+amp)*1.1

	# Generating the probability density graph
	fig, ax = plt.subplots(figsize=(12,9))
	ax.spines['right'].set_color('none')
	ax.xaxis.tick_bottom()
	ax.spines['left'].set_color('none')
	ax.axes.get_yaxis().set_visible(False)
	ax.spines['top'].set_color('none')
	X3 = np.linspace(0.0, L, 900,endpoint=True)
	Emax = En(nmax,L,me)
	ax.axis([-0.5*L,1.5*L,0.0,Etop])
	ax.set_xlabel(r'$X$ (Angstroms)')
	for n in range(1,nmax+1):
	    ax.hlines(En(n,L,me), 0.0, L, linewidth=1.8, linestyle='--', color="black")
	    str1="$n = "+str(n)+r"$, $E_{"+str(n)+r"} = %.3f$ eV"%(En(n,L,me))
	    ax.text(1.03*L, En(n,L,me), str1, fontsize=16, color="black")
	    ax.plot(X3,En(n,L,me)+ amp*(np.sqrt(L/2.0)*psi(X3,n,L))**2, color="red", label="", linewidth=2.8)
	ax.margins(0.00)
	ax.vlines(0.0, 0.0, Etop, linewidth=4.8, color="blue")
	ax.vlines(L, 0.0, Etop, linewidth=4.8, color="blue")
	ax.hlines(0.0, 0.0, L, linewidth=4.8, color="blue")
	plt.title('Probability Density', fontsize=30)
	lgd = plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.)
	str2="$V = +\infty$"
	ax.text(-0.15*L, 0.6*Emax, str2, rotation='vertical', fontsize=40, color="black")

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png', bbox_extra_artists=lgd, bbox_inches='tight')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
