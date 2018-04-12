#!/usr/bin/python
# Encoding: utf8


# Script para reportar la longitud de las secuencias en un fasta.

import matplotlib.pyplot as plt
import sys

delim = ">"


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



input = sys.argv[1]
lista = fasta2list(input, delim)
longitudes, conteos = vector_longitudes(lista)
harry_plotter(longitudes, conteos)
