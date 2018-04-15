#!/usr/bin/python
# Encoding: utf8


# Script para reportar la longitud de las secuencias en un fasta.

import sys
from termcolor import *

delim = ">"
sub = True
min_len_value = 5000

def fasta2list (path, delim):
	a = open(path, "r")
	b = a.read().split(delim)
	return b

def reportar_longitudes (lista_archivo):
	
	higher_100k = 0
	lower_500 = 0

	total = 0	
	for seq in lista_archivo:
		total += 1
		lineas = seq.split("\n")
		if len("".join(lineas[1:])) != 0:
		
			if len("".join(lineas[1:])) > 100000:
				higher_100k += 1
		
			if len("".join(lineas[1:])) < 500:
				lower_500 += 1

			print len("".join(lineas[1:]))


	print
	print colored("Un total de ", "yellow", attrs=["bold"]) + colored(str(total), "yellow", attrs=["bold", "underline"]) + colored(" contigs:", "yellow", attrs=["bold"])
	print colored("\t-", "yellow", attrs=["bold"]) + colored(str(higher_100k), "yellow", attrs=["bold"]) + colored(" superiores a 100k pb.", "yellow", attrs=["bold"])
	print colored("\t-", "yellow", attrs=["bold"]) + colored(str(lower_500), "yellow", attrs=["bold"]) + colored(" inferiores a 500 pb.", "yellow", attrs=["bold"])


a = fasta2list(sys.argv[1], delim)
reportar_longitudes(a)
