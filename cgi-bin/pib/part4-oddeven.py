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
if "a" not in form or "Vo" not in form or "V1" not in form or "d" not in form:
	print("Content-Type: text/html")    # HTML is following
	print()                             # blank line, end of headers
	print("<H1>Error</H1>")
	print("Please fill in the name and addr fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	# Reading the input variables from the user
	Vo = abs(float(form["Vo"].value))
	a =  abs(float(form["L"].value))
	V1 = abs(float(form["V1"].value))
	d =  abs(float(form["d"].value))

	val = np.sqrt(2.0*9.10938356e-31*1.60217662e-19)*1e-10/(1.05457180013e-34) # equal to sqrt(2m*1eV)*1A/hbar

	# Defining functions that come from the energy expression
	def f0(E):
	    var = -np.sqrt(Vo-E)+np.sqrt(E)*np.tan(np.sqrt(E)*val*(d/2.0+a))
	    var = var/(np.sqrt(E)+np.sqrt(Vo-E)*np.tan(np.sqrt(E)*val*(d/2.0+a)))
	    return var

	def f1(E):
	    var = np.sqrt(V1-E)*np.tanh(d*np.sqrt(V1-E)*val/2.0)+np.sqrt(E)*np.tan(d*np.sqrt(E)*val/2.0)
	    var = var/(np.sqrt(E)-np.sqrt(V1-E)*np.tanh(d*np.sqrt(V1-E)*val/2.0)*np.tan(d*np.sqrt(E)*val/2.0))
	    return var

	def f2(E):
	    var = np.sqrt(E)+np.sqrt(Vo-E)*np.tan(np.sqrt(E)*val*(d/2.0+a))
	    var = var/(np.sqrt(E)*np.tan(np.sqrt(E)*val*(d/2.0+a))-np.sqrt(Vo-E))
	    return var

	def f3(E):
	    var = np.sqrt(E)*np.tanh(d*np.sqrt(V1-E)*val/2.0)-np.sqrt(V1-E)*np.tan(d*np.sqrt(E)*val/2.0)
	    var = var/(np.sqrt(V1-E)+np.sqrt(E)*np.tanh(d*np.sqrt(V1-E)*val/2.0)*np.tan(d*np.sqrt(E)*val/2.0))
	    return var

	# Generating the wavefunction graph
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	fig, axes = plt.subplots(1, 2, figsize=(13,4))
	axes[0].axis([0.0,Vo,-np.sqrt(Vo)*1.9,np.sqrt(Vo)*1.9])
	axes[0].set_xlabel(r'$E$ (eV)')
	axes[0].set_ylabel(r'')
	axes[0].set_title('Even solution')
	axes[1].axis([0.0,Vo,-np.sqrt(Vo)*1.9,np.sqrt(Vo)*1.9])
	axes[1].set_xlabel(r'$E$ (eV)')
	axes[1].set_ylabel(r'')
	axes[1].set_title('Odd solution')
	E_even = np.linspace(0.0, Vo, 10000)
	E_odd = np.linspace(0.0, Vo, 10000)
	# Removing discontinuity points
	for n in range(10000):
	    if abs(np.sqrt(E_even[n])+np.sqrt(Vo-E_even[n])*np.tan(np.sqrt(E_even[n])*val*(d/2.0+a)))<0.1: E_even[n] = np.nan
	    if abs(np.sqrt(E_even[n])-np.sqrt(V1-E_even[n])*np.tanh(d*np.sqrt(V1-E_even[n])*val/2.0)*np.tan(d*np.sqrt(E_even[n])*val/2.0))<0.1: E_even[n] = np.nan
	    if abs(np.sqrt(E_odd[n])*np.tan(np.sqrt(E_odd[n])*val*(d/2.0+a))-np.sqrt(Vo-E_odd[n]))<0.1: E_odd[n] = np.nan
	    if abs(np.sqrt(V1-E_odd[n])+np.sqrt(E_odd[n])*np.tanh(d*np.sqrt(V1-E_odd[n])*val/2.0)*np.tan(d*np.sqrt(E_odd[n])*val/2.0))<0.1: E_odd[n] = np.nan
	# Plotting the curves and setting the labelsaxes[0].plot(E_even, f0(E_even), label=r"$\frac{-\alpha_o+k\tan\left[k\left(\frac{d}{2}+a\right)\right]}{k+\alpha_o\tan\left[k\left(\frac{d}{2}+a\right)\right]}$", color="blue")
	axes[0].plot(E_even, f0(E_even), label=r"$\frac{-\alpha_o+k\tan\left[k\left(\frac{d}{2}+a\right)\right]}{k+\alpha_o\tan\left[k\left(\frac{d}{2}+a\right)\right]}$", color="blue")
	axes[0].plot(E_even, f1(E_even), label=r"$\frac{\alpha_1\tanh\left(\alpha_1\frac{d}{2}\right)+k\tan\left(k\frac{d}{2}\right)}{k-\alpha_1\tanh\left(\alpha_1\frac{d}{2}\right)\tan\left(k\frac{d}{2}\right)}$", color="red")
	axes[1].plot(E_odd,  f2(E_odd),  label=r"$\frac{k+\alpha_o\tan\left[k\left(\frac{d}{2}+a\right)\right]}{-\alpha_o+k\tan\left[k\left(\frac{d}{2}+a\right)\right]}$", color="blue")
	axes[1].plot(E_odd,  f3(E_odd),  label=r"$\frac{k\tanh\left(\alpha_1\frac{d}{2}\right)-\alpha_1\tan\left(k\frac{d}{2}\right)}{\alpha_1+k\tanh\left(\alpha_1\frac{d}{2}\right)\tan\left(k\frac{d}{2}\right)}$", color="red")
	# Chosing the positions of the legends
	lgd1 = axes[0].legend(bbox_to_anchor=(0.05, -0.2), loc=2, borderaxespad=0.0)
	lgd2 = axes[1].legend(bbox_to_anchor=(0.05, -0.2), loc=2, borderaxespad=0.0)

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png', bbox_extra_artists=(lgd1,lgd2), bbox_inches='tight')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
