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

	# Generating the energy diagram
	fig, ax = plt.subplots(figsize=(8,12))
	ax.spines['right'].set_color('none')
	ax.yaxis.tick_left()
	ax.spines['bottom'].set_color('none')
	ax.axes.get_xaxis().set_visible(False)
	ax.spines['top'].set_color('none')
	ax.axis([0.0,10.0,0.0,1.1*Vo])
	ax.set_ylabel(r'$E_n$ (eV)')
	for n in range(1,nstates+1):
	    str1="$n = "+str(n)+r"$, $E_"+str(n)+r" = %.3f$ eV"%(E_vals[n-1])
	    ax.text(6.5, E_vals[n-1]-0.005*Vo, str1, fontsize=16, color="red")
	    ax.hlines(E_vals[n-1], 0.0, 6.3, linewidth=1.8, linestyle='--', color="red")
	str1="$V_o = %.3f$ eV"%(Vo)
	ax.text(6.5, Vo-0.01*Vo, str1, fontsize=16, color="blue")
	ax.hlines(Vo, 0.0, 6.3, linewidth=1.8, linestyle='-', color="blue")
	ax.hlines(0.0, 0.0, 10.3, linewidth=1.8, linestyle='-', color="black")
	plt.title("Energy Levels", fontsize=30)
	plt.show()

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
