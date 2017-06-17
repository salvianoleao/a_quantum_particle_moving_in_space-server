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
if "L1" not in form or "L2" not in form or "n" not in form:
	print("Content-Type: text/html")    # HTML is following
	print()                             # blank line, end of headers
	print("<H1>Error</H1>")
	print("Please fill in the name and addr fields.")
else:
	print("Content-Type: image/png")    # HTML is following
	print()                             # blank line, end of headers

	L1 = float(form["L1"].value)
	L2 = float(form["L2"].value)
	n = int(form["n"].value)
	L = 100

	# Defining the wavefunction
	def psi(x,n,L): return np.sqrt(2.0/L)*np.sin(float(n)*np.pi*x/L)

	# Generating the wavefunction and probability density graphs
	plt.rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
	fig, ax = plt.subplots(figsize=(12,6))
	ax.spines['right'].set_color('none')
	ax.xaxis.tick_bottom()
	ax.spines['left'].set_color('none')
	ax.axes.get_yaxis().set_visible(False)
	ax.spines['top'].set_color('none')
	val = 1.1*max(L1,L2)
	X1 = np.linspace(0.0, L1, 900,endpoint=True)
	X2 = np.linspace(0.0, L2, 900,endpoint=True)
	ax.axis([-0.5*val,1.5*val,-np.sqrt(2.0/L),3*np.sqrt(2.0/L)])
	ax.set_xlabel(r'$X$ (Angstroms)')
	strA="$\psi_n$"
	strB="$|\psi_n|^2$"
	ax.text(-0.12*val, 0.0, strA, rotation='vertical', fontsize=30, color="black")
	ax.text(-0.12*val, np.sqrt(4.0/L), strB, rotation='vertical', fontsize=30, color="black")
	str1=r"$L = "+str(L1)+r"$ A"
	str2=r"$L = "+str(L2)+r"$ A"
	ax.plot(X1,psi(X1,n,L1)*np.sqrt(L1/L), color="red", label=str1, linewidth=2.8)
	ax.plot(X2,psi(X2,n,L2)*np.sqrt(L2/L), color="blue", label=str2, linewidth=2.8)
	ax.plot(X1,psi(X1,n,L1)*psi(X1,n,L1)*(L1/L) + np.sqrt(4.0/L), color="red", linewidth=2.8)
	ax.plot(X2,psi(X2,n,L2)*psi(X2,n,L2)*(L2/L) + np.sqrt(4.0/L), color="blue", linewidth=2.8)
	ax.margins(0.00)
	ax.legend(loc=9)
	str2="$V = +\infty$"
	ax.text(1.03*val,  0.5*np.sqrt(2.0/L), str2, rotation='vertical', fontsize=40, color="black")
	ax.text(-0.3*val, 0.5*np.sqrt(2.0/L), str2, rotation='vertical', fontsize=40, color="black")
	ax.vlines(0.0, -np.sqrt(2.0/L), 2.5*np.sqrt(2.0/L), linewidth=4.8, color="red")
	ax.vlines(L1, -np.sqrt(2.0/L), 2.5*np.sqrt(2.0/L), linewidth=4.8, color="red")
	ax.vlines(0.0, -np.sqrt(2.0/L), 2.5*np.sqrt(2.0/L), linewidth=4.8, color="blue")
	ax.vlines(L2, -np.sqrt(2.0/L), 2.5*np.sqrt(2.0/L), linewidth=4.8, color="blue")
	ax.hlines(0.0, 0.0, L, linewidth=1.8, linestyle='--', color="black")
	ax.hlines(np.sqrt(4.0/L), 0.0, L, linewidth=1.8, linestyle='--', color="black")
	plt.title('Wavefunction and Probability Density', fontsize=30)
	str3=r"$n = "+str(n)+r"$"
	ax.text(1.1*L,np.sqrt(4.0/L), r"$n = "+str(n)+r"$", fontsize=25, color="black")
	plt.legend(bbox_to_anchor=(0.73, 0.95), loc=2, borderaxespad=0.)

	# Show the plots on the screen once the code reaches this point
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)  # rewind the data
	sys.stdout.flush()
	sys.stdout.buffer.write(buf.getvalue())
