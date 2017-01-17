#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import cgi
import cgitb
cgitb.enable()

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers


form = cgi.FieldStorage()
if "n" not in form or "L" not in form:
	print("<H1>Error</H1>")
	print("Please fill in the n and L fields.")
else:
	print("<p>name:", form["name"].value)
	print("<p>addr:", form["addr"].value)
print("hello world!!!")
