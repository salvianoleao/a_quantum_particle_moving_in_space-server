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
	a =  abs(float(form["a"].value))
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

	# We want to find the values of E in which f_even and f_odd are zero
	f_even = lambda E : f0(E)-f1(E)
	f_odd = lambda E : f2(E)-f3(E)
	E_old = 0.0
	f_even_old = f_even(0.0)
	f_odd_old = f_odd(0.0)
	n_even = 1
	n_odd = 1
	E_vals = np.zeros(999)
	n = 1
	# Here we loop from E = 0 to E = Vo seeking roots
	for E in np.linspace(0.0, Vo, 20000):
	    f_even_now = f_even(E)
	    # If the difference is zero or if it changes sign then we might have passed through a root
	    if (f_even_now == 0.0 or f_even_now/f_even_old < 0.0):
	        # If the old values of f are not close to zero, this means we didn't pass through a root but
	        # through a discontinuity point
	        if (abs(f_even_now)<1.0 and abs(f_even_old)<1.0):
	            E_vals[n-1] = (E+E_old)/2.0
	            n += 1
	            n_even += 1
	    f_odd_now = f_odd(E)
	    # If the difference is zero or if it changes sign then we might have passed through a root
	    if (f_odd_now == 0.0 or f_odd_now/f_odd_old < 0.0) and (E>0.0):
	        # If the old values of f are not close to zero, this means we didn't pass through a root but
	        # through a discontinuity point
	        if (abs(f_odd_now)<1.0 and abs(f_odd_old)<1.0):
	            E_vals[n-1] = (E+E_old)/2.0
	            n += 1
	            n_odd += 1
	    E_old = E
	    f_even_old = f_even_now
	    f_odd_old = f_odd_now
	nstates = n-1

	# Drawing the backgroung graph
	fig, ax = plt.subplots(figsize=(12,9))
	ax.spines['right'].set_color('none')
	ax.xaxis.tick_bottom()
	ax.spines['left'].set_color('none')
	ax.axes.get_yaxis().set_visible(False)
	ax.spines['top'].set_color('none')
	ax.axis([-1.5*a-d/2.0,1.5*a+d/2.0,0.0,1.15*Vo])
	ax.set_xlabel(r'$X$ (Angstroms)')
	str1="$V_o = %.3f$ eV"%(Vo)
	ax.text(1.05*(a+d/2.0), 1.02*Vo, str1, fontsize=24, color="blue")
	# Defining the maximum amplitude of the wavefunction
	if ((E_vals[1]-E_vals[0])/(E_vals[2]-E_vals[0]) < 0.2):
	    amp = np.sqrt((E_vals[2]-E_vals[0])/1.5)
	else:
	    amp = np.sqrt((E_vals[1]-E_vals[0])/1.5)
	# Plotting the energy levels
	for n in range(1,nstates+1):
	    ax.hlines(E_vals[n-1], -1.5*a-d/2.0, 1.5*a+d/2.0, linewidth=1.8, linestyle='--', color="black")
	ax.margins(0.00)
	ax.vlines(-a-d/2.0, 0.0, Vo, linewidth=4.8, color="blue")
	if(d>0.0):
	    ax.vlines(-d/2.0, 0.0, V1, linewidth=4.8, color="blue")
	    ax.vlines(d/2.0, 0.0, V1, linewidth=4.8, color="blue")
	ax.vlines(a+d/2.0, 0.0, Vo, linewidth=4.8, color="blue")
	ax.hlines(Vo, -1.5*a-d/2.0, -a-d/2.0, linewidth=4.8, color="blue")
	ax.hlines(0.0, -a-d/2.0, -d/2.0, linewidth=4.8, color="blue")
	ax.hlines(V1, -d/2.0, d/2.0, linewidth=4.8, color="blue")
	ax.hlines(0.0, d/2.0, a+d/2.0, linewidth=4.8, color="blue")
	ax.hlines(Vo, a+d/2.0, 1.5*a+d/2.0, linewidth=4.8, color="blue")
	plt.title('Probability Densities for even states', fontsize=30)
	plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.)

	# Defining the X ranges
	X_lef2 = np.linspace(-1.5*a-d/2.0, -a-d/2.0, 900,endpoint=True)
	X_lef1 = np.linspace(-a-d/2.0, -d/2.0, 900,endpoint=True)
	X_mid = np.linspace(-d/2.0, d/2.0, 900,endpoint=True)
	X_rig1 = np.linspace(d/2.0, a+d/2.0, 900,endpoint=True)
	X_rig2 = np.linspace(a+d/2.0, 1.5*a+d/2.0, 900,endpoint=True)

	# Plotting the probability densities
	for n in range(1,nstates+1):
	    k = np.sqrt(E_vals[n-1])*val
	    a0 = np.sqrt(Vo-E_vals[n-1])*val
	    a1 = np.sqrt(V1-E_vals[n-1])*val
	    str1="$n = "+str(n)+r"$, $E_{"+str(n)+r"} = %.3f$ eV"%(E_vals[n-1])
	    # Odd wavefunction
	    if (n%2==0):
	        C = amp/np.sqrt(f3(E_vals[n-1])*f3(E_vals[n-1])+1.0)
	        B = f3(E_vals[n-1])*C
	        A = (B*np.cos(k*d/2.0)+C*np.sin(k*d/2.0))/(-np.exp(-a1*d/2.0)+np.exp(a1*d/2.0))
	        D = np.exp(a0*(a+d/2.0))*(B*np.cos(k*(a+d/2.0))+C*np.sin(k*(a+d/2.0)))
	        ax.plot(X_lef2, E_vals[n-1]+(D*np.exp(a0*X_lef2))**2, color="red", label="", linewidth=2.8)
	        ax.fill_between(X_lef2, E_vals[n-1], E_vals[n-1]+(D*np.exp(a0*X_lef2))**2, color="green")
	        ax.plot(X_lef1, E_vals[n-1]+(-B*np.cos(k*X_lef1)+C*np.sin(k*X_lef1))**2, color="red", label="", linewidth=2.8)
	        ax.plot(X_mid,  E_vals[n-1]+(A*(-np.exp(-a1*X_mid)+np.exp(a1*X_mid)))**2, color="red", label="", linewidth=2.8)
	        ax.fill_between(X_mid, E_vals[n-1], E_vals[n-1]+(A*(-np.exp(-a1*X_mid)+np.exp(a1*X_mid)))**2, color="purple")
	        ax.plot(X_rig1, E_vals[n-1]+(B*np.cos(k*X_rig1)+C*np.sin(k*X_rig1))**2, color="red", label="", linewidth=2.8)
	        ax.plot(X_rig2, E_vals[n-1]+(D*np.exp(-a0*X_rig2))**2, color="red", label="", linewidth=2.8)
	        ax.fill_between(X_rig2, E_vals[n-1], E_vals[n-1]+(D*np.exp(-a0*X_rig2))**2, color="green")
	        ax.text(1.05*(a+d/2.0), E_vals[n-1]+0.01*Vo, str1, fontsize=16, color="black")

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
