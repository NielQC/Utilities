#!/usr/bin/python
# Encoding: utf8


# Script para reportar por terminal la longitud de las secuencias en un fasta.
# Está pensado para assemblies. 

import sys
from termcolor import *
import argparse

parser = argparse.ArgumentParser(description="Reporta la longitud de las lecturas en un fasta. Está pensado para assemblies, aunque se puede utilizar con cualquier multifasta")

parser.add_argument("-d", "--delimiter", default=">", help="Caracter para spliter el multifasta en las secuencias individuales (default: '>')")
parser.add_argument("-max", help="Umbral de longitud superior para reportar por terminal (default: 100k)", default= 100000, type= int)
parser.add_argument("-min", help="Umbral de longitud inferior para reportar por terminal (default: 500)", default= 500, type = int) 
parser.add_argument("FASTA")
parser.add_argument('--version', action='version', version='April, 2018')

args = parser.parse_args()


## Función para leer el archivo y devolver una lista con las secuencias
def fasta2list (file, delim):
	a = open(file, "r")
	b = a.read().split(delim)
	return b

## Función que coge la lista proporcionada por la función anterior, 
## calcula las longitudes y reporta
def reportar_longitudes (lista_archivo, min_value, max_value):
	
	higher = 0
	lower = 0

	total = 0	
	for seq in lista_archivo:
		total += 1
		lineas = seq.split("\n")
		if len("".join(lineas[1:])) != 0:
		
			if len("".join(lineas[1:])) > max_value:
				higher += 1
		
			if len("".join(lineas[1:])) < min_value:
				lower += 1

			print len("".join(lineas[1:]))


	print
	print colored("Un total de ", "yellow", attrs=["bold"]) + colored(str(total), "yellow", attrs=["bold", "underline"]) + colored(" contigs:", "yellow", attrs=["bold"])
	print colored("\t- ", "yellow", attrs=["bold"]) + colored(str(higher), "yellow", attrs=["bold"]) + colored(" superiores a ", "yellow", attrs=["bold"]) + colored(str(max_value) + " pb.", "yellow", attrs=["bold"])
	print colored("\t- ", "yellow", attrs=["bold"]) + colored(str(lower), "yellow", attrs=["bold"]) + colored(" inferiores a ", "yellow", attrs=["bold"]) + colored(str(min_value) + " pb.", "yellow", attrs=["bold"])


##########
#  Main  #
##########

def main():

	a = fasta2list(args.FASTA, args.delimiter)
	reportar_longitudes(a, args.min, args.max)

if __name__ == "__main__":
    main()


