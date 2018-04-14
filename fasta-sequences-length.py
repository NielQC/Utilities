#!/usr/bin/python
# Encoding: utf8


# Script para reportar la longitud de las secuencias en un fasta.

import matplotlib.pyplot as plt
import sys

delim = ">"
sub = True
min_len_value = 5000

def fasta2list (path, delim):
	a = open(path, "r")
	b = a.read().split(delim)
	return b

def vector_longitudes (lista_archivo):
	dic = dict()

	for seq in lista_archivo:
		lineas = seq.split("\n")
		longi = len("".join(lineas[1:]))

		if longi in dic:
			dic[longi] += 1
		else:
			dic[longi] = 1

	x = list()
	y = list()

	for k, v in dic.items():
		x.append(k)
		y.append(v)

	return x, y

def harry_plotter (x, y):

	print x
	print y
	plt.bar(x, y)
	plt.show()

def harry_plotter_2 (x, y, threshold):

	lower_x = list()
	lower_y = list()
	higher_x = list()
	higher_y = list()

	for i in range(len(x)):
		if x < threshold:
			lower_x.append(x[i])
			lower_y.append(y[i])
		else:
			higher_x.append(x[i])
			higher_y.append(y[i])

	f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
	ax1.bar(lower_x, lower_y)
	ax1.set_title('Sharing Y axis')
	ax2.bar(higher_x, higher_y)



input = sys.argv[1]
lista = fasta2list(input, delim)
longitudes, conteos = vector_longitudes(lista)
harry_plotter_2(longitudes, conteos, min_len_value)



