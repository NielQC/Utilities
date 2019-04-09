# Encoding: utf8

####
# Script para crear los links.
# Input: 	- genomas a comparar
# Output:	- Carpeta nucmer
#        	- Archivo nucmer/links.txt
# Modifica:	- Archivo circos.conf
####

import os
import glob
import errno
import os
import random

path = os.getcwd()

palete = ["RdYlGn-11-div-9", "RdYlGn-11-div-8", "RdYlGn-11-div-9", "RdYlGn-11-div-6", "RdYlGn-11-div-4", "RdYlGn-11-div-3", "RdYlGn-11-div-2"]

##############################################
def crear_carpeta(path):
	
	try:
	    os.mkdir(path)
	except OSError as exc:
	    if exc.errno != errno.EEXIST:
		raise
	    pass

#############################################
def listaclean(lista):
	while "" in lista:
		lista.remove("")

	return lista

#############################################
def lanzar_nucmer(archivo1, archivo2, circosdir, minlength, nucmer_path):
	crear_carpeta("%s/nucmer" % (circosdir))
	
	os.system("%s -p %s/nucmer/out %s %s" % (nucmer_path, circosdir, archivo1, archivo2))
	os.system("show-coords -q -T -H -L %s %s/nucmer/out.delta > %s/nucmer/coords.txt" % (minlength, circosdir, circosdir))

#############################################
def crear_linkstxt(circosdir, palete):
	with open("%s/nucmer/coords.txt"% (circosdir)) as datos:
		lineas = datos.readlines()

		i = 0
		with open("%s/nucmer/links.txt"% (circosdir), "w") as out:
			for linea in lineas:
				campos = linea.strip().split("\t")

				color = palete[i]
				out.write("%s\t%s\t%s\t%s\t%s\t%s\tcolor=%s\n" % (campos[-2], campos[0], campos[1], campos[-1], campos[3], campos[2], color))
				i += 1

#############################################				
def modificar_conf(circosdir):
	with open("%s/circos.conf" % (circosdir)) as datos:
		lineas = datos.readlines()

		tow = ["<links>\n", "<link>\n", "ribbon = yes\n", "file          = %s/nucmer/links.txt\n" % (circosdir), "radius        = 0.82r\n" , "stroke_color = dgrey\n", "stroke_thickness = 2\n", "bezier_radius = 0r\n", "</link>\n", "</links>\n"] 
 			
		with open("%s/circos.conf" % (circosdir), "w") as out:
			for linea in lineas:
				if "# $LINKS" in linea:
					out.write("%s\n" % ("".join(tow)))

				else:
					out.write(linea)

############################################
def lanzar_circos(circosdir):
	os.system("circos -noparanoid -conf %s/circos.conf" % (circosdir))

############################################

def main():
   
	output_folder = "Circos"
	nucmer_path = "nucmer"
	lanzar_nucmer("fasta/GCF_000009045.1_ASM904v1_genomic.fna", "fasta/GCF_001565875.1_ASM156587v1_genomic.fna", output_folder, 6000, nucmer_path)

	palete = ["blues-9-seq-2", "blues-9-seq-3", "blues-9-seq-4", "blues-9-seq-5", "blues-9-seq-6", "blues-9-seq-7"] * 1000
	crear_linkstxt(output_folder, palete)
	modificar_conf(output_folder)

	lanzar_circos(output_folder)
	

 
if __name__ == "__main__":
    main()

