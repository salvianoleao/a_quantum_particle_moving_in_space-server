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
if "L1" not in form or "L2" not in form or "n1" not in form or "n2" not in form:
	print("Content-Type: text/html")    # HTML is following
	print()                             # blank line, end of headers
	print("<H1>Error</H1>")
	print("Please fill in the name and addr fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	L1 = int(form["L1"].value)
	L2 = int(form["L2"].value)
	nmax1 = int(form["n1"].value)
	nmax2 = int(form["n2"].value)
	
	# Defining a function to compute the energy
	def En(n,L): return 37.60597*((float(n)/L)**2)

	# Generating the graph
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	fig, ax = plt.subplots(figsize=(8,12))
	ax.spines['right'].set_color('none')
	ax.yaxis.tick_left()
	ax.spines['bottom'].set_color('none')
	ax.axes.get_xaxis().set_visible(False)
	ax.spines['top'].set_color('none')
	val = 1.1*max(En(nmax1,L1),En(nmax2,L2))
	val2= 1.1*max(L1,L2)
	ax.axis([0.0,10.0,0.0,val])
	ax.set_ylabel(r'$E_n$ (eV)')
	for n in range(1,nmax1+1):
		str1="$n = "+str(n)+r"$, $E_{"+str(n)+r"} = %.3f$ eV"%(En(n,L1))
		ax.text(0.6, En(n,L1)+0.01*val, str1, fontsize=16, color="red")
		ax.hlines(En(n,L1), 0.0, 4.5, linewidth=1.8, linestyle='--', color="red")
	for n in range(1,nmax2+1):
		str1="$n = "+str(n)+r"$, $E_{"+str(n)+r"} = %.3f$ eV"%(En(n,L2))
		ax.text(6.2, En(n,L2)+0.01*val, str1, fontsize=16, color="blue")
		ax.hlines(En(n,L2), 5.5, 10.0, linewidth=1.8, linestyle='--', color="blue")
	str1=r"$L = "+str(L1)+r"$ A"
	plt.title("Energy Levels \n ", fontsize=30)
	str1=r"$L = "+str(L1)+r"$ A"
	str2=r"$L = "+str(L2)+r"$ A"
	ax.text(1.5,val, str1, fontsize=25, color="red")
	ax.text(6,val, str2, fontsize=25, color="blue")

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
