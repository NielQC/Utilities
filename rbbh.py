#!/usr/bin/python
# Encoding: utf8
# Dani Carrillo Bautista

# Script para hacer un análisis de Reciprocal Blast Best Hits (RBBH) entre dos archivos.

from termcolor import *
import argparse, os

parser = argparse.ArgumentParser(description="Realiza un análisis RBBH con los archivos fasta proporcionados.")

parser.add_argument("A", help="Primer archivo FASTA.")
parser.add_argument("B", help="Segundo archivo FASTA.")
parser.add_argument("-o", "--output")
parser.add_argument("-id", "--identity", help="Porcentaje de identidad umbral (default: 90)", default=90, type=int)
parser.add_argument("-cov", "--coverage", help="Porcentaje de coverage umbral para la secuencia query (default: 50)", default=50, type=int)
parser.add_argument("-mode", help="Modo 'prot' o 'nucl' (default: 'prot').", default="prot", choices=["prot", "nucl"])
parser.add_argument("-t", "--threads", help="Número de threads a utilizar durante la etapa de blast (default: 16)", default=16)
parser.add_argument("-blast", help="Path hacia el binario de blast (default: 'blastp')", default="blastp")
parser.add_argument("-makeblastdb", help="Path hacia el binario de makeblastdb (default: 'makeblastdb')", default="makeblastdb")

parser.add_argument('--version', action='version', version='April, 2018')

args = parser.parse_args()


##
def crear_directorios (path, file_A, file_B):
	if not os.path.exists(os.path.abspath(path)):
		os.makedirs(os.path.abspath(path))
	if not os.path.exists(os.path.abspath(path) + "/" + file_A):
		os.makedirs(os.path.abspath(path) + "/" + file_A + "/db")
	if not os.path.exists(os.path.abspath(path) + "/" + file_B):
		os.makedirs(os.path.abspath(path) + "/" + file_B + "/db")

##
def makeblastdb (path, file_A, file_B, makeblastdb_path, mode):
	os.system("sed -i 's/ /_/g' %s" % (file_A))
	os.system("sed -i 's/\t>/_/g' %s" % (file_A))
	os.system("sed -i 's/ /_/g' %s" % (file_B))
	os.system("sed -i 's/\t>/_/g' %s" % (file_B))

	os.system("%s -in %s -out %s -dbtype %s" % (makeblastdb_path, file_A, os.path.abspath(path) + "/" + file_A.split("/")[-1] + "/db/" + file_A.split("/")[-1], mode))
	os.system("%s -in %s -out %s -dbtype %s" % (makeblastdb_path, file_B, os.path.abspath(path) + "/" + file_B.split("/")[-1] + "/db/" + file_B.split("/")[-1], mode))
	
##
def blast (path, file_A, file_B, mode, blast_path, threads):
	if mode == "nucl" and blast_path == "blastp":
		blast_path = "blastn"
	
	os.system("%s -query %s -db %s -num_threads %s -num_alignments 1 -evalue 1e-5 -outfmt '6 qaccver saccver pident length qcovhsp mismatch gapopen qlen qstart qend slen sstart send evalue' -out %s" % (blast_path, file_A, os.path.abspath(path) + "/" + file_B.split("/")[-1] + "/db/" + file_B.split("/")[-1], threads, os.path.abspath(path) + "/" + file_A.split("/")[-1] + "/" + file_A.split("/")[-1].split(".")[0] + "_query.blast"))
	os.system("sort -k3,5 -n -r -o %s %s" % (os.path.abspath(path) + "/" + file_A.split("/")[-1] + "/" + file_A.split("/")[-1].split(".")[0] + "_query.blast", os.path.abspath(path) + "/" + file_A.split("/")[-1] + "/" + file_A.split("/")[-1].split(".")[0] + "_query.blast"))

	os.system("%s -query %s -db %s -num_threads %s -num_alignments 1 -evalue 1e-5 -outfmt '6 qaccver saccver pident length qcovhsp mismatch gapopen qlen qstart qend slen sstart send evalue' -out %s" % (blast_path, file_B, os.path.abspath(path) + "/" + file_A.split("/")[-1] + "/db/" + file_A.split("/")[-1], threads, os.path.abspath(path) + "/" + file_B.split("/")[-1] + "/" + file_B.split("/")[-1].split(".")[0] + "_query.blast"))
	os.system("sort -k3,5 -n -r -o %s %s" % (os.path.abspath(path) + "/" + file_B.split("/")[-1] + "/" + file_B.split("/")[-1].split(".")[0] + "_query.blast", os.path.abspath(path) + "/" + file_B.split("/")[-1] + "/" + file_B.split("/")[-1].split(".")[0] + "_query.blast"))

##
def reciprocal(path, file_A, file_B, identity, coverage):
	dict_A = dict()
	for linea in open(os.path.abspath(path) + "/" + file_A.split("/")[-1] + "/" + file_A.split("/")[-1].split(".")[0] + "_query.blast", "r"):
		campos = linea.split("\t")
		if float(campos[2]) > identity and float(campos[4]) > coverage:
			if campos[0] not in dict_A:
				dict_A[campos[0]] = campos[1]
	
	dict_B = dict()
	for linea in open(os.path.abspath(path) + "/" + file_B.split("/")[-1] + "/" + file_B.split("/")[-1].split(".")[0] + "_query.blast", "r"):
		campos = linea.split("\t")
		if float(campos[2]) > identity and float(campos[4]) > coverage:
			if campos[0] not in dict_B:
				dict_B[campos[0]] = campos[1]

	

	total_A = dict()
	total_B = dict()
	
	x = open(file_A, "r")
	y = x.read().split(">")
	y.remove("")
	for gen in y:
		lineas = gen.split("\n")
		total_A[lineas[0]] = "\n".join(lineas[1:])
	
	x = open(file_B, "r")
	y = x.read().split(">")
	y.remove("")
	for gen in y:
		lineas = gen.split("\n")
		total_B[lineas[0]] = "\n".join(lineas[1:])
		
	shared_A = list()
	shared_B = list()

	for k,v in dict_A.items():
		if v in dict_B:
			if dict_B[v] == k:
				shared_A.append(k)
				shared_B.append(v)
	
	unique_A = list()
	unique_B = list()
	for gen in total_A:
		if gen not in shared_A:
			unique_A.append(gen)
	for gen in total_B:
		if gen not in shared_B:
			unique_B.append(gen)

	shared_A_out = open(os.path.abspath(path) + "/shared_" + file_A.split("/")[-1], "w")
	shared_B_out = open(os.path.abspath(path) + "/shared_" + file_B.split("/")[-1], "w")
	unique_A_out = open(os.path.abspath(path) + "/unique_" + file_A.split("/")[-1], "w")
	unique_B_out = open(os.path.abspath(path) + "/unique_" + file_B.split("/")[-1], "w")
	shared_table = open(os.path.abspath(path) + "/shared-table.txt", "w")


	for gen in total_A:
		if gen in shared_A:
			shared_A_out.write(">" + gen + "\n" + total_A[gen] + "\n")
		else:	
			unique_A_out.write(">" + gen + "\n" + total_A[gen] + "\n")
			
	for gen in total_B:
		if gen in shared_B:
			shared_B_out.write(">" + gen + "\n" + total_B[gen] + "\n")
		else:	
			unique_B_out.write(">" + gen + "\n" + total_B[gen] + "\n")
	
	for i in range(len(shared_A)):
		shared_table.write(shared_A[i] + "\t" + shared_B[i] + "\n")		


	perc_shared_A = (len(shared_A) * 100.0) / len(total_A)
	perc_shared_B = (len(shared_B) * 100.0) / len(total_B)
	perc_unique_A = (len(unique_A) * 100.0) / len(total_A)
	perc_unique_B = (len(unique_B) * 100.0) / len(total_B)

	
	print
	print colored("Archivo ", "yellow", attrs=["bold"]) + colored(str(file_A.split("/")[-1]), "yellow", attrs=["bold", "underline"]) + colored(":", "yellow", attrs=["bold"])
	print colored("\t- Secuencias totales: %d" % len(total_A), "yellow", attrs=["bold"])
	print colored("\t- Secuencias compartidas: %d" % len(shared_A), "yellow", attrs=["bold"]) + colored(" (%0.2f %%)" % perc_shared_A, "cyan")
	print colored("\t- Secuencias exclusivas:  %d" % len(unique_A), "yellow", attrs=["bold"]) + colored(" (%0.2f %%)" % perc_unique_A, "cyan")
	print 
	print colored("Archivo ", "yellow", attrs=["bold"]) + colored(str(file_B.split("/")[-1]), "yellow", attrs=["bold", "underline"]) + colored(":", "yellow", attrs=["bold"])
	print colored("\t- Secuencias totales: %d" % len(total_B), "yellow", attrs=["bold"])
	print colored("\t- Secuencias compartidas: %d" % len(shared_B), "yellow", attrs=["bold"]) + colored(" (%0.2f %%)" % perc_shared_B, "cyan")
	print colored("\t- Secuencias exclusivas:  %d" % len(unique_B), "yellow", attrs=["bold"]) + colored(" (%0.2f %%)" % perc_unique_B, "cyan")
	print
		


def main():
	crear_directorios(args.output, args.A, args.B)
	makeblastdb(args.output, args.A, args.B, args.makeblastdb, args.mode)
	blast(args.output, args.A, args.B, args.mode, args.blast, args.threads)
	reciprocal(args.output, args.A, args.B, args.identity, args.coverage)

if __name__ == "__main__":
    main()
