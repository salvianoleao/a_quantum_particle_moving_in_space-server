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
if "L" not in form or "Vo" not in form:
	print("Content-Type: text/html")    # HTML is following
	print()                             # blank line, end of headers
	print("<H1>Error</H1>")
	print("Please fill in the name and addr fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	# Reading the input variables from the user
	Vo = float(form["Vo"].value)
	L =  float(form["L"].value)

	val = np.sqrt(2.0*9.10938356e-31*1.60217662e-19)*1e-10/(2.0*1.05457180013e-34) # equal to sqrt(2m*1eV)*1A/(2*hbar)

	# We want to find the values of E in which f_even and f_odd are zero
	f_even = lambda E : np.sqrt(Vo-E)-np.sqrt(E)*np.tan(L*np.sqrt(E)*val)
	f_odd = lambda E : np.sqrt(Vo-E)+np.sqrt(E)/np.tan(L*np.sqrt(E)*val)
	E_old = 0.0
	f_even_old = f_even(0.0)
	f_odd_old = f_odd(0.0)
	n = 1
	E_vals = np.zeros(999)
	# Here we loop from E = 0 to E = Vo seeking roots
	for E in np.linspace(0.0, Vo, 20000):
	    f_even_now = f_even(E)
	    # If the difference is zero or if it changes sign then we might have passed through a root
	    if f_even_now == 0.0 or f_even_now/f_even_old < 0.0:
	        # If the old values of f are not close to zero, this means we didn't pass through a root but
	        # through a discontinuity point
	        if (abs(f_even_now)<1.0 and abs(f_even_old)<1.0):
	            E_vals[n-1] = (E+E_old)/2.0
	            n += 1
	    f_odd_now = f_odd(E)
	    # If the difference is zero or if it changes sign then we might have passed through a root
	    if f_odd_now == 0.0 or f_odd_now/f_odd_old < 0.0:
	        # If the old values of f are not close to zero, this means we didn't pass through a root but
	        # through a discontinuity point
	        if (abs(f_odd_now)<1.0 and abs(f_odd_old)<1.0):
	            E_vals[n-1] = (E+E_old)/2.0
	            n += 1
	    E_old = E
	    f_even_old = f_even_now
	    f_odd_old = f_odd_now
	nstates = n-1

	fig, ax = plt.subplots(figsize=(12,9))
	ax.spines['right'].set_color('none')
	ax.xaxis.tick_bottom()
	ax.spines['left'].set_color('none')
	ax.axes.get_yaxis().set_visible(False)
	ax.spines['top'].set_color('none')
	X_lef = np.linspace(-L, -L/2.0, 900,endpoint=True)
	X_mid = np.linspace(-L/2.0, L/2.0, 900,endpoint=True)
	X_rig = np.linspace(L/2.0, L, 900,endpoint=True)
	ax.axis([-L,L,0.0,1.1*Vo])
	ax.set_xlabel(r'$X$ (Angstroms)')
	str1="$V_o = %.3f$ eV"%(Vo)
	ax.text(1.05*L/2.0, 1.02*Vo, str1, fontsize=24, color="blue")
	# Defining the maximum amplitude of the probability density
	if (nstates > 1):
	    amp = (E_vals[1]-E_vals[0])/1.5
	else:
	    amp = (Vo-E_vals[0])/1.5
	# Plotting the probability densities
	for n in range(1,nstates+1):
	    ax.hlines(E_vals[n-1], -L, L, linewidth=1.8, linestyle='--', color="black")
	    str1="$n = "+str(n)+r"$, $E_"+str(n)+r" = %.3f$ eV"%(E_vals[n-1])
	    ax.text(1.2*L/2.0, E_vals[n-1]+0.01*Vo, str1, fontsize=16, color="black")
	    k = 2.0*np.sqrt(E_vals[n-1])*val
	    a0 = 2.0*np.sqrt(Vo-E_vals[n-1])*val
	    # Plotting odd probability densities
	    if (n%2==0):
	        Y_lef = E_vals[n-1]+amp*(np.exp(a0*L/2.0)*np.sin(k*L/2.0)*np.exp(a0*X_lef))**2
	        ax.plot(X_lef,Y_lef, color="red", label="", linewidth=2.8)
	        ax.fill_between(X_lef, E_vals[n-1], Y_lef, color="green")
	        ax.plot(X_mid,E_vals[n-1]+amp*(np.sin(k*X_mid))**2, color="red", label="", linewidth=2.8)
	        Y_rig = E_vals[n-1]+amp*(np.exp(a0*L/2.0)*np.sin(k*L/2.0)*np.exp(-a0*X_rig))**2
	        ax.plot(X_rig,Y_rig, color="red", label="", linewidth=2.8)
	        ax.fill_between(X_rig, E_vals[n-1], Y_rig, color="green")
	    # Plotting even probability densities
	    else:
	        Y_lef = E_vals[n-1]+amp*(np.exp(a0*L/2.0)*np.cos(k*L/2.0)*np.exp(a0*X_lef))**2
	        ax.plot(X_lef,Y_lef, color="red", label="", linewidth=2.8)
	        ax.fill_between(X_lef, E_vals[n-1], Y_lef, color="green")
	        ax.plot(X_mid,E_vals[n-1]+amp*(np.cos(k*X_mid))**2, color="red", label="", linewidth=2.8)
	        Y_rig = E_vals[n-1]+amp*(np.exp(a0*L/2.0)*np.cos(k*L/2.0)*np.exp(-a0*X_rig))**2
	        ax.plot(X_rig,Y_rig, color="red", label="", linewidth=2.8)
	        ax.fill_between(X_rig, E_vals[n-1], Y_rig, color="green")
	ax.margins(0.00)
	ax.vlines(-L/2.0, 0.0, Vo, linewidth=4.8, color="blue")
	ax.vlines(L/2.0, 0.0, Vo, linewidth=4.8, color="blue")
	ax.hlines(0.0, -L/2.0, L/2.0, linewidth=4.8, color="blue")
	ax.hlines(Vo, -L, -L/2.0, linewidth=4.8, color="blue")
	ax.hlines(Vo, L/2.0, L, linewidth=4.8, color="blue")
	plt.title('Probability Densities', fontsize=30)
	plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.)


	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
