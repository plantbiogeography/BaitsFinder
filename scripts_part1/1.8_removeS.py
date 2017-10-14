#!usr/bin/python
import os,os.path
file1=open("ITAG.-2.vs.Mguttatus.-2")
file2=open("ITAG.arabidopsis.single.gene.list.-2")
file3=open("ITAG_nohit","a")
lines1=file1.readlines()
gene1=[]
for line1 in lines1:
	line1=line1.split("\t")
	gene1.append(line1[0])
gene1=list(set(gene1)) 
lines2=file2.readlines()
gene2=[]
for line2 in lines2: 
	line2=line2.rstrip()
	gene2.append(line2)	
gene1specif=list(set(gene1).difference(set(gene2)))
gene2specif=list(set(gene2).difference(set(gene1)))
specif=gene1specif+gene2specif
for i in specif:
	file3.write(i+"\n")
file1.close()
file2.close()
file3.close()
