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
	def psi_contour(x,dk): return (2.0*np.sin(dk*x)/x)
	def psi(x,k,dk): return psi_contour(x,dk)*(np.cos(k*x)+np.sin(k*x)*1j)

	k = float(form["k"].value)
	xmax = float(form["xmax"].value)
	dk = float(form["dk"].value)

	# Generating the wavefunction graph
	lim1 = 2.0*dk
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	x = np.linspace(-xmax, xmax, 900)
	fig, axes = plt.subplots(1, 2, figsize=(13,4))
	str1=r"$k_o  \pm \Delta k$ = "+str(k)+r" $\pm$ "+str(dk)+r" A$^{-1}$"
	# axes[0] is the graph at the left
	axes[0].axis([-xmax,xmax,-1.1*lim1,1.1*lim1])
	axes[0].plot(x, psi(x,k,dk).real, label="Real", color="blue", linewidth=1.8)
	axes[0].plot(x, psi_contour(x,dk), label="", linestyle ="--",color="blue", linewidth=1.2)
	axes[0].plot(x, -psi_contour(x,dk), label="", linestyle ="--",color="blue", linewidth=1.2)
	axes[0].hlines(0.0, -xmax, xmax, linewidth=1.8, linestyle='--', color="black")
	axes[0].set_xlabel(r'$x$ (Angstroms)')
	axes[0].set_ylabel(r'$Real(\Psi_{\Delta k}(x))$')
	axes[0].set_title('Real contribution to $\Psi_{\Delta k}(x)$ \n for '+str1)
	# axes[1] is the graph at the right
	axes[1].axis([-xmax,xmax,-1.1*lim1,1.1*lim1])
	axes[1].plot(x, psi(x,k,dk).imag, label="Imag.", color="red", linewidth=1.8)
	axes[1].plot(x, psi_contour(x,dk), label="", linestyle ="--",color="red", linewidth=1.2)
	axes[1].plot(x, -psi_contour(x,dk), label="", linestyle ="--",color="red", linewidth=1.2)
	axes[1].hlines(0.0, -xmax, xmax, linewidth=1.8, linestyle='--', color="black")
	axes[1].yaxis.set_label_position("right")
	axes[1].set_xlabel(r'$x$ (Angstroms)')
	axes[1].set_ylabel(r'$Imag(\Psi_{\Delta k}(x))$')
	axes[1].set_title('Imaginary contribution to $\Psi_{\Delta k}(x)$ \n for '+str1)

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
