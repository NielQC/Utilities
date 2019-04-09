# Encoding: utf8

####
# Script para crear los ideogramas.
# Input: genomas a comparar
# Output: - Carpeta karyotypes
#         - Archivo circos.conf
#         - Archivo idogramas.conf
#         - Archivo ticks.conf
# Depend: - Biopython (GCcalc)
#         - termcolor
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
def fasta2karyotype(archivo_fasta, name, palete, circosdir, hide):
	with open(archivo_fasta) as datos:
		data = datos.read()
		contigs = listaclean(data.split(">"))

		color = random.choice(palete)
		cont = 1		
	
		with open("%s/karyotypes/%s.karyo" % (circosdir, name), "w") as out:
			for contig in contigs:
				lineas = listaclean(contig.split("\n"))
				
				code = lineas[0].split(" ")[0].split("\t")[0]
				length = len("".join(lineas))

				if length < 70000:
					hide.append(code)
					

				out.write("chr - %s %s_%d 0 %d %s\n" % (code, name, cont, length, color  ) )

				cont += 1
		

############################################
def crear_circos_conf(ruta_conf_modelo, circosdir):
	with open(ruta_conf_modelo) as datos:
		
		karyos = glob.glob("%s/karyotypes/*.karyo" % (circosdir))

		lineas = datos.readlines()
		lineas[0] = lineas[0].strip() + " %s\n" % (",".join(karyos))
	
	with open("%s/circos.conf" % (circosdir), "w") as out:
		for linea in lineas:
			out.write(linea)

############################################
def crear_ideo_conf(ruta_ideo_modelo, circosdir, hide):

	tow = list()
	for code in hide:
		tow.append("label_format     = eval( var(chr) eq '%s' ? '' : var(label))" % (code))

	with open(ruta_ideo_modelo) as datos:
		lineas = datos.readlines()

		with open("%s/ideogram.conf" % (circosdir), "w") as out:
			for linea in lineas:
				if "# $HIDE" in linea:
					out.write("\n".join(tow))
				else:
					out.write(linea)

############################################
def crear_ticks_conf(ruta_ticks_modelo, circosdir):
	os.system("cp %s %s/ticks.conf" % (ruta_ticks_modelo, circosdir))


############################################
def lanzar_circos(circosdir):
	os.system("circos -noparanoid -conf %s/circos.conf" % (circosdir))

############################################

def main():
   
	output_folder = "Circos"

	crear_carpeta(output_folder)
	crear_carpeta("%s/karyotypes" % (output_folder))

	archivos = ["fasta/GCF_000009045.1_ASM904v1_genomic.fna", "fasta/GCF_001565875.1_ASM156587v1_genomic.fna"] #, "fasta/GCF_001022195.1_ASM102219v1_genomic.fna"]
	nombres = ["BPL34", "ATCC14931", "AS-16"]
	palete = ["RdYlGn-11-div-9", "RdYlGn-11-div-8", "RdYlGn-11-div-9", "RdYlGn-11-div-6", "RdYlGn-11-div-4", "RdYlGn-11-div-3", "RdYlGn-11-div-2"]

	os.system("rm Circos/karyotypes/*.karyo")
	
	cont = 0
	hide_list = list()
	for archivo in archivos:
		fasta2karyotype(archivo, nombres[cont], palete, output_folder, hide_list)
		cont += 1

	print hide_list

	conf_modelo = "/home/dani/GitHub/Utilities/circos.conf_modelo"
	ideo_modelo = "/home/dani/GitHub/Utilities/ideogram.conf_modelo"
	ticks_modelo = "/home/dani/GitHub/Utilities/ticks.conf_modelo"
	crear_circos_conf(conf_modelo, output_folder)
	crear_ideo_conf(ideo_modelo, output_folder, hide_list)
	crear_ticks_conf(ticks_modelo, output_folder)

	lanzar_circos(output_folder)

 
if __name__ == "__main__":
    main()




