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
	print("Please fill in the name and addr fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	# Defining functions
	def psi_contour(x,dk): return (4.0*np.sin(dk*x)*np.sin(dk*x)/(x*x))
	def psi_contourG(x,dk): return (2.0*np.pi*dk*dk*np.exp(-x*x*dk*dk))

	k = float(form["k"].value)
	xmax = float(form["xmax"].value)
	dk = float(form["dk"].value)

	# Generating the probability density graphs
	lim0 = 4.0*dk*dk
	lim1 = psi_contourG(0,dk)
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	x = np.linspace(-xmax, xmax, 900)
	fig, axes = plt.subplots(1, 2, figsize=(13,7))
	str1=r"$k_o \pm \Delta k$ = "+str(k)+r" $\pm$ "+str(dk)+r" A$^{-1}$"
	axes[0].plot(x, psi_contour(x,dk), label="", linestyle ="-",color="green", linewidth=1.8)
	axes[0].hlines(0.0, -xmax, xmax, linewidth=1.8, linestyle='--', color="black")
	axes[0].axis([-xmax,xmax,-0.1*lim0,1.1*lim0])
	axes[0].set_xlabel(r'$x$ (Angstroms)')
	axes[0].set_ylabel(r'$\left|\Psi_k(x)\right|^2$')
	axes[0].set_title('Probability Density \n for '+str1)
	axes[1].plot(x, psi_contourG(x,dk), label="", linestyle ="-",color="magenta", linewidth=1.8)
	axes[1].hlines(0.0, -xmax, xmax, linewidth=1.8, linestyle='--', color="black")
	axes[1].axis([-xmax,xmax,-0.1*lim1,1.1*lim1])
	axes[1].set_xlabel(r'$x$ (Angstroms)')
	axes[1].set_ylabel(r'$\left|\Psi_k(x)\right|^2$')
	axes[1].set_title('Probability Density \n for '+str1)

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
