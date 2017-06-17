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
	print("Content-Type: text/plain")    # HTML is following
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

	print ("\nThe tunneling probabilities and probabilities of being inside the barrier are:")
	for n in range(1,nstates+1):
	    k = np.sqrt(E_vals[n-1])*val
	    a0 = np.sqrt(Vo-E_vals[n-1])*val
	    a1 = np.sqrt(V1-E_vals[n-1])*val
	    # Odd wavefunction
	    if (n%2==0):
	        C = 1.0
	        B = f3(E_vals[n-1])*C
	        D = np.exp(a0*(a+d/2.0))*(B*np.cos(k*(a+d/2.0))+C*np.sin(k*(a+d/2.0)))
	        tunn_prob = D*D*np.exp(-a0*(2.0*a+d))/(2.0*a0)
	        total_prob = tunn_prob
	        if (d>0.0):
	            A = (B*np.cos(k*d/2.0)+C*np.sin(k*d/2.0))/(-np.exp(-a1*d/2.0)+np.exp(a1*d/2.0))
	            barr_prob = A*A*(np.sinh(a1*d)/a1-d)
	            total_prob += barr_prob
	        else:
	            barr_prob = 0.0
	        total_prob += (B*B*(np.sin(k*(2.0*a+d))+2.0*a*k-np.sin(k*d))+2.0*B*C*(np.cos(k*d)-np.cos(k*(2.0*a+d)))+C*C*(-np.sin(k*(2.0*a+d))+2.0*a*k+np.sin(k*d)))/(4.0*k)
	        print ("  State #%3d  (Odd): tunneling probability = %5.2f%%, barrier probability = %5.2f%%" % (n,100*tunn_prob/total_prob,100*barr_prob/total_prob))
	    # Even wavefunction
	    else:
	        B = 1.0
	        C = f1(E_vals[n-1])*B
	        A = (B*np.cos(k*d/2.0)+C*np.sin(k*d/2.0))/(np.exp(-a1*d/2.0)+np.exp(a1*d/2.0))
	        D = np.exp(a0*(a+d/2.0))*(B*np.cos(k*(a+d/2.0))+C*np.sin(k*(a+d/2.0)))
	        barr_prob = A*A*(np.sinh(a1*d)/a1+d)
	        tunn_prob = D*D*np.exp(-a0*(2.0*a+d))/(2.0*a0)
	        total_prob = barr_prob + tunn_prob
	        total_prob += (B*B*(np.sin(k*(2.0*a+d))+2.0*a*k-np.sin(k*d))+2.0*B*C*(np.cos(k*d)-np.cos(k*(2.0*a+d)))+C*C*(-np.sin(k*(2.0*a+d))+2.0*a*k+np.sin(k*d)))/(4.0*k)
	        print ("  State #%3d (Even): tunneling probability = %5.2f%%, barrier probability = %5.2f%%" % (n,100*tunn_prob/total_prob,100*barr_prob/total_prob))
