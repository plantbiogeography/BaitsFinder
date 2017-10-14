#!usr/bin/python
import os,os.path
file1=open("1456519283nogap.fas.1.out")
file2=open("1456519283nogap.fas.1")
file3=open("1456519283nogap.fas.list","a")
file4=open("1456519283nogap.fas.1.plastid_free","a")
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
