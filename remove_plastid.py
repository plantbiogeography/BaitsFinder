#!usr/bin/python

import os,os.path
import sys
import getopt

## get args from command line
## -r : output from step 7.2 (e.g. 1456519283nogap.fas.1)
## -s : output from step 7.3 (e.g. 1456519283nogap.fas.1.out)
## -o : output preffix
opts,args = getopt.getopt(sys.argv[1:],"r:s:o:")
for op, value in opts:
    if op == "-r":
        blast_in = str(value)
    if op == "-s":
        blast_out = str(value)
    if op == "-o":
        preffix = str(value)

file1=open(blast_out)
file2=open(blast_in)
file3=open(preffix + ".list","a")
file4=open(preffix + ".plastid_free","a")
lines1=file1.readlines()
gene1=[]
for line1 in lines1:
	line=line1.split("\t")
	if(float(line[7])>=90):
	          gene1.append(line[3]+"\t"+line[4])
gene1=list(set(gene1)) 
for i in gene1:
	file3.write(i+"\n")
lines2=file2.readlines()
gene2=[]
num=1
for line2 in lines2:
	if (num==0):
		file4.write(line2)
	gene2=line2.split("\t")
	if (">" in line2):
		if ((gene2[3]+"\t"+gene2[4]) in gene1):
			num=1
		else:
			file4.write(line2);num=0
	else:
		num=1
file1.close()
file2.close()
file3.close()
file4.close()
