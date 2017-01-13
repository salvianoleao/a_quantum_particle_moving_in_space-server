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
if "n" not in form or "m" not in form or "Lx" not in form or "Ly" not in form:
	print("Content-Type: text/html")    # HTML is following
	print()                             # blank line, end of headers
	print("<H1>Error</H1>")
	print("Please fill in the name and addr fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	nmax1 = int(form["n"].value)
	L1 = int(form["Lx"].value)
	mmax2 = int(form["m"].value)
	L2 = int(form["Ly"].value)

	# Defining the wavefunction
	def psi2D(x,y): return 2.0*np.sin(n*np.pi*x)*np.sin(m*np.pi*y)
	# Defining the energy as a function
	def En2D(n,m,L1,L2): return 37.60597*((float(n)/L1)**2+ (float(m)/L2)**2)
	
	# Plotting the energy levels
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	fig, ax = plt.subplots(figsize=(nmax1*2+2,nmax1*3))
	ax.spines['right'].set_color('none')
	ax.yaxis.tick_left()
	ax.spines['bottom'].set_color('none')
	ax.axes.get_xaxis().set_visible(False)
	ax.spines['top'].set_color('none')
	val = 1.1*(En2D(nmax1,mmax2,L1,L2))
	val2= 1.1*max(L1,L2)
	ax.axis([0.0,3*nmax1,0.0,val])
	ax.set_ylabel(r'$E_n$ (eV)')
	for n in range(1,nmax1+1):
		for m in range(1, mmax2+1):
			str1="$n,m = "+str(n)+r","+str(m)+r"$"
			str2=" $E = %.3f$ eV"%(En2D(n,m,L1,L2))
			ax.text(n*2-2, En2D(n,m,L1,L2)+ 0.005*val, str1, fontsize=16, color="blue")
			ax.hlines(En2D(n,m,L1,L2), n*2-2, n*2-0.5, linewidth=3.8, color="red")
			ax.hlines(En2D(n,m,L1,L2), 0.0, nmax1*2+1, linewidth=1., linestyle='--', color="black")
			ax.text(nmax1*2+1, En2D(n,m,L1,L2)+ 0.005*val, str2, fontsize=16, color="blue")
	plt.title("Energy Levels \n ", fontsize=30)
	str1=r"$L_x = "+str(L1)+r"$ A, $n_{max} = "+str(nmax1)+r"$     $L_y = "+str(L2)+r"$ A,  $m_{max}="+str(mmax2)+r"$"
	ax.text(1.5,val, str1, fontsize=25, color="black")

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
