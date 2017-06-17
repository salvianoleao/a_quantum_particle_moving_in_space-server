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
	print("Content-Type: text/plain")    # HTML is following
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

	print ("\nThe tunneling probabilities are:")
	for n in range(1,nstates+1):
	    k = 2.0*np.sqrt(E_vals[n-1])*val
	    a0 = 2.0*np.sqrt(Vo-E_vals[n-1])*val
	    # For odd solution
	    if (n%2==0):
	        C = 1.0
	        D = np.exp(a0*L/2.0)*np.sin(k*L/2.0)*C
	        prob = D*D*2.0*k*np.exp(-a0*L)/(B*B*a0*(k*L-np.sin(k*L))+D*D*2.0*k*np.exp(-a0*L))
	    # For even solution
	    else:
	        B = 1.0
	        D = np.exp(a0*L/2.0)*np.cos(k*L/2.0)*B
	        prob = D*D*2.0*k*np.exp(-a0*L)/(B*B*a0*(k*L+np.sin(k*L))+D*D*2.0*k*np.exp(-a0*L))
	    print("  State #%3d tunneling probability = %5.2f%%" % (n,100*prob))
