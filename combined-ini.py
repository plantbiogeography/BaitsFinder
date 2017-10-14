#-*- encoding: utf-8 -*-
import commands
import platform
import sys
import os,os.path
import ctypes
import csv
import glob
import math
import numpy as np
import scipy as sp
import shutil
import traceback
#import globalvar
from functools import partial
from multiprocessing import cpu_count


CPU_n1=cpu_count()
CPU_n2=str(max(1,CPU_n1))


plat=platform.platform()

path=os.path.abspath(os.curdir)
config=path.replace('\\','/')+'/config.ini'
CRC0=os.path.exists(config)
if  'Windows' not in plat and 'Linux'  not in plat:
    #warning notice, if this script was not running in linux or windows!
    print('\033[1;31;40m')
    print('*' * 49)
    print('***Please USE this script in Linux or windows!!!***')
    print('*' * 49)
    print('\033[0m')
    exit(0)

elif "Linux" in plat:
    Sys_ver="L"

elif 'Windows' in plat:
    Sys_ver='W'
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE= -11
    STD_ERROR_HANDLE = -12
    FOREGROUND_BLACK = 0x0
    FOREGROUND_BLUE = 0x01 
    FOREGROUND_GREEN= 0x02 
    FOREGROUND_RED = 0x04 
    FOREGROUND_INTENSITY = 0x08 
    BACKGROUND_BLUE = 0x10
    BACKGROUND_GREEN= 0x20 
    BACKGROUND_RED = 0x40 
    BACKGROUND_INTENSITY = 0x80 
    class Color:
        ''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
        for information on Windows APIs. '''
        std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        def set_cmd_color(self, color, handle=std_out_handle):
            """(color) -> bit
            Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
            """
            bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
            return bool
        def reset_color(self):
            self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
        def print_red_text(self, print_text):
            self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
            print print_text
            self.reset_color()
        def print_green_text(self, print_text):
            self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
            print print_text
            self.reset_color()
        def print_blue_text(self, print_text):
            self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
            print print_text
            self.reset_color()
        def print_red_text_with_blue_bg(self, print_text):
            self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY| BACKGROUND_BLUE | BACKGROUND_INTENSITY)
            print print_text
            self.reset_color()  

if os.path.exists(config)==0:
    if Sys_ver=='L':
        print('\033[1;31;40m')
        print('*' * 73)
        print('***Please make sure you have the config.ini file in current folder!!!***')
        print('*' * 73)
        print('\033[0m')
    else:
        if __name__ == "__main__":
            clr = Color()
            clr.print_red_text('*'*73)
            clr.print_red_text('***Please make sure you have the config.ini file in current folder!!!***')
            clr.print_red_text('*'*73)
    exit(0)
con_file=open(config).readlines()
CRC0=0
CRC1=0
CRC2=0
rFAAnames = []
rGFFnames=[]
sFNAnames=[]
host1={}
host2={}
sufficient=[]
sorted_length=0
sorted_host_by_identity=0
baits_length=0
for line in con_file:
    if '##' not in line:
        if 'RAW_path' in line:
            CRC0+=1
            RAW_path=line.replace('\\','/').split('=')[1].strip()+'/'
            RAW_path=RAW_path.replace('//','/')
        elif 'Tem_path' in line:
            CRC0+=1
            Tem_path=line.replace('\\','/').split('=')[1].strip()+'/'
            Tem_path=Tem_path.replace('//','/')
        elif 'Out_path' in line:
            CRC0+=1
            Out_path=line.replace('\\','/').split('=')[1].strip()+'/'
            Out_path=Out_path.replace('//','/')
        elif 'Mafft_path' in line:
            CRC0+=1
            Mafft_path=line.replace('\\','/').split('=')[1].strip()+'/'
            Mafft_path=Mafft_path.replace('//','/')
        elif 'Blast_path' in line:
            CRC0+=1
            Blast_path=line.split('=')[1].strip()+'/'
            Blast_path=Blast_path.replace('//','/')
        elif 'Blast_ver' in line:
            CRC0+=1
            Blast_ver=line.split('=')[1].strip()
        elif 'Blast_gap' in line:
            CRC0+=1
            Blast_gap=line.split('=')[1].strip()
        elif 'rFAAnames' in line:
            CRC0+=1
            rFAAnames.append(line.split('=')[1].strip())
        elif 'rFNAname' in line:
            CRC0+=1
            rFNAname=line.split('=')[1].strip()
        elif 'rGFFnames' in line:
            CRC0+=1
            rGFFnames.append(line.split('=')[1].strip())
        elif 'sFNAnames' in line:
            CRC0+=1
            CRC1+=1
            sFNAnames.append(line.split('=')[1].strip())
            host1[line.split('=')[1].strip()]='0'
            host2[line.split('=')[1].strip()]=''
        elif '=host_name=' in line:
            CRC0+=1
            CRC2+=1
            a0=line.split('=')[0].strip()
            a1=line.split('=')[2].strip()
            host2[a0]=a1
            if a1 !='NAN':
                host1[a0]='1'
        elif 'sorted_length'  in line:
            a0=line.split('=')[1].strip()
            sorted_length=eval(a0)
        elif 'sorted_host_by_identity' in line:
            a0=line.split('=')[1].strip()
            sorted_host_by_identity=float(a0)
        elif 'sufficient_data' in line:
            a0=line.split('=')[1].strip()
            if a0!='NAN':
                sufficient.append(a0)
        elif 'baits_length' in line:
            a0=line.split('=')[1].strip()
            baits_length=eval(a0)
if CRC0==0 or CRC2!=CRC1 :
    if Sys_ver=='L':
        print('\033[1;31;40m')
        print('*' * 73)
        print('***Please make sure you have the config.ini file in current folder!!!***')
        print('*' * 73)
        print('\033[0m')
    else:
        if __name__ == "__main__":
            clr = Color()
            clr.print_red_text('*'*73)
            clr.print_red_text('***Please make sure you have the config.ini file in current folder!!!***')
            clr.print_red_text('*'*73)
    exit(0)
if os.path.exists(Tem_path)==0:
    os.makedirs(Tem_path)        
files=os.listdir(RAW_path)
shutil.rmtree(Tem_path,True)
if os.path.exists(Tem_path)==0:
    os.makedirs(Tem_path)
for fname in files:
    shutil.copyfile(RAW_path+fname,Tem_path+fname)


## 2.3. Combine the all_hits files of each query taxon  into a single file
i0=0
tcl_files=os.listdir(RAW_path)
Tem_path2=Tem_path+'cleaned/'
Tem_path3=Tem_path+'combined/'
TemL=[]
if os.path.exists(Tem_path2)==0:
    os.makedirs(Tem_path2)
if os.path.exists(Tem_path3)==0:
    os.makedirs(Tem_path3)
for fname in tcl_files:
    if 'out.all_hits' in fname:
        i0=i0+1
        lines=open(Tem_path+fname).readlines()
        myfile2=open(Tem_path2+fname,'w')
        for line in lines:
            a1=line.split()[1]
            if 'no_hits_found' in a1:
                continue
            else:
                myfile2.write(line)
                TemL.append(line)
myfile2.close()
if Blast_gap=='1':
    all_hits=str(i0)+'_all_hits_nogap'
elif Blast_gap=='2':
    all_hits=str(i0)+'_all_hits_gap'
myfile=open(Tem_path3+all_hits,'w')
for line in TemL:
    myfile.write(line)
myfile.close()


## 2.4. Remove putative contamination.
## 2.4.1. Construct a joint list of putative contamaninant sequences
## 2.4.2. Merge contaminant sequences into a single file
## 2.4.3. Remove contaminant sequences
CRC3=0
for i1 in host1.values():
    i2=eval(i1)
    CRC3=CRC3+i2
if CRC3!=0:
    if os.path.exists(Tem_path+'all_host'):
        os.remove(Tem_path+'all_host')
    all_host=open(Tem_path+'all_host','a')
    for fname in sFNAnames:        
        pver=host1[fname]
        if pver=='1':
            gene=[]
            hname=host2[fname]
            fname2=fname.split('.')[0]+'.sort_'+hname[:2]+'.out'
            

            lines=open(Tem_path+fname2).readlines()
            myfile=open(Tem_path+fname2+'.sort',"a")
            for line in lines:
                line=line.split("\t")
                if(float(line[2])>=sorted_host_by_identity):
                    gene.append(line[0])
            gene=list(set(gene))
            for i in gene:
                myfile.write(i+"\n")
                all_host.write(i+"\n")
            myfile.close()
    all_host.close()

    files=os.listdir(Tem_path)
    lines=open(Tem_path+'all_host').readlines()
    host_gid=[]
    for line in lines:
        a0=line.split()[0]
        host_gid.append(a0)
    for fname in files:
        if 'ungap.out.matrix.identity' in fname:
            output_file21=str.lower(fname[:2])+'_ungap_host_free'
            lines=open(Tem_path+fname).readlines()
            myfile=open(Tem_path+output_file21,'w')
            for line in lines:
                a1=line.split()[0]
                if a1 not in host_gid:
                    myfile.write(line)        
            myfile.close()
        elif 'gap.out.matrix.identity' in fname:
            output_file21=str.lower(fname[:2])+'_gap_host_free'
            lines=open(Tem_path+fname).readlines()
            myfile=open(Tem_path+output_file21,'w')
            for line in lines:
                a1=line.split()[0]
                if a1 not in host_gid:
                    myfile.write(line)        
            myfile.close()
    print "Host-removed has been finished sucessfully!!"
else:
    for fname in files:
        if 'ungap.out.matrix.identity' in fname:
            output_file21=str.lower(fname[:2])+'_ungap_host_free'
            lines=open(Tem_path+fname).readlines()
            myfile=open(Tem_path+output_file21,'w')
            for line in lines:
                myfile.write(line)        
            myfile.close()
        elif 'gap.out.matrix.identity' in fname:
            output_file21=str.lower(fname[:2])+'_gap_host_free'
            lines=open(Tem_path+fname).readlines()
            myfile=open(Tem_path+output_file21,'w')
            for line in lines:
                myfile.write(line)        
            myfile.close()
            

## 2.5. Identify and remove putative paralogues.
## 2.5.1. Add position information to matrix files
files=os.listdir(Tem_path)
lines2=open(Tem_path+'combined/'+all_hits).readlines()
for fname in files:
    if ('_ungap_host_free' in fname or '_gap_host_free' in fname) and '.add' not in fname:
        d=[]
        output_file22=fname+'.add'
        lines1=open(Tem_path+fname).readlines()
        myfile=open(Tem_path+output_file22,'w')
        for line in lines1:
            a0=line.split()[0]+'\t'+line.split()[1]+'\t'+line.split()[2]+'\t'+line.split()[3]+'\t'+line.split()[4]
            d.append(a0)
        for line in lines2:
            a1=line.split()[0]+'\t'+line.split()[1]+'\t'+str(float(line.split()[3])/100)+'\t'+line.split()[2]+'\t'+line.split()[5]
            a2=line.split()[0]+'\t'+line.split()[10]+'\t'+line.split()[11]+'\t'+line.split()[1]+'\t'+str(3*eval(line.split()[12])-2)+'\t'+str(3*eval(line.split()[13]))+'\t'+line.split()[-1]+'\t'+str(float(line.split()[3])/100)+'\n'
            if a1 in d:
                myfile.write(a2)
        myfile.close()

## 2.5.2. Identify overlapping sequences from focal species that blast against the same reference gene
        lines=open(Tem_path+output_file22).readlines()
        output_file23=output_file22+'.sorted'
        output_file24=output_file23+'.paralogInfo'
        output_file25=output_file24+'.out'
        myfile=open(Tem_path+output_file23,'w')
        d=[]
        f={}
        x=0
        for line in lines:
            d.append(line.split())
            y=str(x)
            f[y]=''
            x=x+1
        d2=sorted(d, key=lambda result: (result[3],eval(result[4])),reverse=False)

        for i in d2:
            i1=str(i)
            j=''
            for k in i1.split():
                j=j+k+'\t'
            j=j[:-1]+'\n'
            j=j.replace('[','')
            j=j.replace(']','')
            j=j.replace('\'','')
            j=j.replace(',','')
            myfile.write(j)
        myfile.close()

        lines=open(Tem_path+output_file23).readlines()
        myfile=open(Tem_path+output_file24,'w')
        ls=len(lines)
        for i in range(1,ls):
            l1=lines[i-1]
            l2=lines[i]
            z1=l1.split()[3]
            z2=l2.split()[3]
            z3=l1.split()[5]
            z4=l2.split()[4]
            if z1==z2 and (eval(z3)-eval(z4))>sorted_length:
                f[str(i-1)]='PARALOG!'
                f[str(i)]='PARALOG!'

        for i in range(ls):
            l1=lines[i]
            if f[str(i)]=='PARALOG!':
                l2=l1[:-1]+'\tPARALOG!\n'
            else:
                l2=l1
            myfile.write(l2)
        myfile.close()


## 2.5.3. Remove putative paralogues using a custom python script
        lines=open(Tem_path+output_file24).readlines()
        myfile=open(Tem_path+output_file25,'w')
        over_bp=str(sorted_length)  ##length of overlap
        f={}
        d=[]
        for line in lines:
            if len(line.split())>3:
                a1=line.split()[3]
                if 'PARALOG' in line:
                    d.append(a1)
        for line in lines:
            if len(line.split())>3:
                a1=line.split()[3]
                if a1 not in d:
                    myfile.write(line)
        myfile.close()

## 2.5.4. Combine the paralogue-free data
all_host_free=[]
files=os.listdir(Tem_path)
i2=0
for fname in files:
    if '.sorted.paralogInfo.out' in fname:
        i2=i2+1
        lines=open(Tem_path+fname).readlines()
        for line in lines:
            all_host_free.append(line)
if Blast_gap=='1':
    fname3=str(i2)+'_nogap_hostfree_'+over_bp+'sorted'
elif Blast_gap=='2':
    fname3=str(i2)+'_gap_hostfree_'+over_bp+'sorted'
myfile=open(Tem_path+fname3,'w')
for line in all_host_free:
    
    myfile.write(line)
myfile.close()

print "Part.2 has been finished successfully!!"


## 3.1. Extract sequences of the non-paralogues genes from each of the focal species
lines=open(Tem_path+fname3).readlines()
for fname in sFNAnames :
    iD=fname.split('.')[0]
    if Blast_gap=='1':
        output_file31=fname.split('.')[0]+'.nogap_edit.codons.query_all.seq'
    elif Blast_gap=='2':
        output_file31=fname.split('.')[0]+'.gap_edit.codons.query_all.seq'
    lines1=open(Tem_path+fname).readlines()
    myfile=open(Tem_path+output_file31,'w')
    x=0
    f={}
    y=''
    for line in lines1:
        if '>' in line:
            if x==1:
                f[a0]=y
                y=''
            a0=line.split()[0][1:]
            x=1
        else:
            y=y+line.split()[0]
    f[a0]=y

    for line in lines:
        if iD in line:
            a0=line.split()[0]
            a1=line.split()[1]
            a2=line.split()[2]
            a3=line.split()[3]
            a4=line.split()[4]
            a5=line.split()[5]
            a6=line.split()[6]
            a7=line.split()[7]
            a8=eval(a1)
            a9=eval(a2)
            b=f[a0]
            if eval(a1)>eval(a2):
                b1=b[a9-1:a8]
            
                c0=' mod: 0.0 reverse '
            else:
                c0=' mod: t0.0 forward '
                b1=b[a8-1:a9]
            e1='>'+a0+' length: '+str(abs(eval(a1)-eval(a2)+1))+c0+a1+'-'+a2+' ['+a3+' '+a4+'-'+a5+']\n'
            e2=b1+'\n'
            myfile.write(e1)
            myfile.write(e2)
    myfile.close()


## 3.2. Combine, per gene, sequences of the reference species and of all focal species into a single file
if os.path.exists(Tem_path+'group1')==0:
    os.mkdir(Tem_path+'group1')
Tem_path3=Tem_path+'/group1/'
lines1=open(Tem_path+fname3).readlines()
output_file32=fname3+'.map'
myfile=open(Tem_path+output_file32,'w')
d=[]
f={}
f1={}
f2={}
f3={}
f4={}
for line in lines1:
    a0=line.split()[0]
    a1=line.split()[1]
    a2=line.split()[2]
    a3=line.split()[3]
    a4=eval(line.split()[4])
    a5=eval(line.split()[5])
    a6=a0+'*'+a1+'-'+a2
    if a3 not in d:
        d.append(a3)
        f3[a3]=a4
        f4[a3]=a5
        f[a3]=a6
    else:
        f3[a3]=min(f3[a3],a4)
        f4[a3]=max(f4[a3],a5)
        f[a3]=f[a3]+'\t'+a6
for i in d:
    myfile.write(i+'\t||\t'+f[i]+'\n')
myfile.close()

lines2=open(RAW_path+rFNAname).readlines()
g={}
b0=''
b1=''
b2=0
for line in lines2:
    if '>' in line:
        if b2 !=0:
            g[b0]=b1+'\n'
            b1=''
        b0=line.split()[0][1:]
            
        b2=1
    else:
        b1=b1+line.split()[0]
g[b0]=b1+'\n'



files=os.listdir(Tem_path)
x={}
x1={}
for fname in files:
    if '.nogap_edit.codons.query_all.seq' in fname:
        lines=open(Tem_path+fname).readlines()
        ls=len(lines)/2
        for i in range(ls):
            l1=lines[2*i]
            l2=lines[2*i+1]
            y0=l1.split()[0][1:]+'*'+l1.split()[6]
            y1=l1.split()[0][1:]+'*'+l1.split()[6]+'*'+l1.split()[-4]+'*'+l1.split()[-2]+'*'+l1.split()[-1]
            x[y0]=l2
            x1[y0]=y1
    if '.gap_edit.codons.query_all.seq' in fname:
        lines=open(Tem_path+fname).readlines()
        ls=len(lines)/2
        for i in range(ls):
            l1=lines[2*i]
            l2=lines[2*i+1]
            y0=l1.split()[0][1:]+'*'+l1.split()[6]
            y1=l1.split()[0][1:]+'*'+l1.split()[6]+'*'+l1.split()[-4]+'*'+l1.split()[-2]+'*'+l1.split()[-1]
            x[y0]=l2
            x1[y0]=y1
for i in d:
    myfile=open(Tem_path3+i+'.fa','w')
    myfile.write('>'+i+'\t'+str(f3[i])+'-'+str(f4[i])+'\n')
    myfile.write(g[i][(f3[i]-1):f4[i]]+'\n')
    j=f[i]
    for k in j.split():
        myfile.write('>'+x1[k].replace('*','\t')+'\n')
        myfile.write(x[k])
    myfile.close()


## 3.3 Bring sequences to the same orientation relative to the reference species
if os.path.exists(Tem_path+'group2')==0:
    os.mkdir(Tem_path+'group2')
rootdir1=Tem_path+'/group1/'
rootdir2=Tem_path+'/group2/'
files=os.listdir(Tem_path+'/group1/')
f={}
f['A']='T'
f['T']='A'
f['U']='A'
f['C']='G'
f['G']='C'
f['N']='N'
for file1 in files:
    lines=open(rootdir1+file1).readlines()
    myfile=open(rootdir2+file1,'w')
    ls=len(lines)/2
    for i in range(ls):
        l1=lines[2*i]
        l2=lines[2*i+1]
        if 'reverse' not in l1:
            myfile.write(l1)
            myfile.write(l2)
        else:
            myfile.write(l1)
            l3=''
            for j in l2[:-1][::-1]:
                l3=l3+f[j]
            l3=l3+'\n'
            myfile.write(l3)
    myfile.close()     

## 3.4. Retain only genes with data from the best-quality focal species
if len(sufficient)>0:
    if os.path.exists(Tem_path+'group3')==0:
        os.mkdir(Tem_path+'group3')
    rootdir1=Tem_path+'/group2/'
    rootdir2=Tem_path+'/group3/'
    files=os.listdir(Tem_path+'/group2/')
    for file1 in files:
        x=0
        lines=open(rootdir1+file1).readlines()
        for line in lines:
            for i in sufficient:
                j=i.split('.')[0]
                if j in line:
                    x=1
        if x==1:
            myfile=open(rootdir2+file1,'w')
            for line in lines:
                myfile.write(line)
        myfile.close()
else:
    if os.path.exists(Tem_path+'group3')==0:
        os.mkdir(Tem_path+'group3')
    rootdir1=Tem_path+'/group2/'
    rootdir2=Tem_path+'/group3/'
    files=os.listdir(rootdir1)
    for fname in files:
        shutil.copyfile(rootdir1+fname,rootdir2+fname)

print "Part.3 has been finished successfully!!"

if Blast_gap=='1':    
## 4.u1. Align sequences of the focal species and the reference species using information on start and end points of the BLAST alignment
    if os.path.exists(Tem_path+'group5')==0:
        os.mkdir(Tem_path+'group5')
    rootdir1=Tem_path+'/group3/'
    rootdir2=Tem_path+'/group5/'
    files=os.listdir(Tem_path+'/group3/')
    for file1 in files:
        lines=open(rootdir1+file1).readlines()
        myfile=open(rootdir2+file1,'w')
        a0=lines[0].split()[-1]
        a1=eval(a0.split('-')[0])
        a2=eval(a0.split('-')[1])
        l3='*'.join(lines[0].split())+'*length='+str(a2-a1+1)+'\n'
        myfile.write(l3)
        myfile.write(lines[1])
        ls=len(lines)/2
        for i in range(1,ls):
            l1=lines[2*i]
            l2=lines[2*i+1][:-1]
            b0=l1.split()[-1][:-1]
            b1=eval(b0.split('-')[0])
            b2=eval(b0.split('-')[1])
            c1=min(b1,b2)
            c2=max(b1,b2)
            l1='*'.join(l1.split())+'*length='+str(c2-c1+1)+'\n'
            myfile.write(l1)
            for i in range(a1,c1):
                l2='-'+l2
            for i in range(c2,a2):
                l2=l2+'-'
            myfile.write(l2+'\n')
        myfile.close()
    
elif Blast_gap=='2':
## 4.g1. Align sequences of the focal species and the reference species using MAFFT
    if os.path.exists(Tem_path+'mafft_out')==0:
        os.mkdir(Tem_path+'mafft_out')
    rootdir1=Tem_path+'/group3/'
    rootdir2=Tem_path+'/mafft_out/'
    myfile0=open('Mafft_error.log','w')

    files=os.listdir(Tem_path+'group3')
    for file1 in files:
        if Sys_ver=='L':
            val= os.system('mafft --ep 0 --genafpair --maxiterate 1000 '+rootdir1+file1+ '>' +rootdir2+file1)
        elif Sys_ver=='W':
            val= os.system(Mafft_path+'mafft.bat --ep 0 --genafpair --maxiterate 1000 '+rootdir1+file1+ '>' +rootdir2+file1)
        if val!=0:
            myfile0.write(file1+'\n')
    myfile0.close()
   
## 4.g2. Change the MAFFT output from multi-line to single-line fasta
    if os.path.exists(Tem_path+'group4')==0:
        os.mkdir(Tem_path+'group4')
    rootdir1=Tem_path+'/mafft_out/'
    rootdir2=Tem_path+'/group4/'
    files=os.listdir(Tem_path+'/mafft_out/')
    for file1 in files:
        x=0
        lines=open(rootdir1+file1).readlines()
        myfile=open(rootdir2+file1,'w')
        for line in lines:
            if '>' in line:
                if x!=0:
                    myfile.write('\n')
                else:
                    x=1
                myfile.write(line)
            else:
                myfile.write(line.split()[0])
        myfile.write('\n')
        myfile.close()

                
## 4.g3. Change white spaces in the sequence titles to asterisks
    if os.path.exists(Tem_path+'group5')==0:
        os.mkdir(Tem_path+'group5')
    rootdir1=Tem_path+'/group4/'
    rootdir2=Tem_path+'/group5/'
    files=os.listdir(Tem_path+'/group4/')
    for file1 in files:
        lines=open(rootdir1+file1).readlines()
        myfile=open(rootdir2+file1,'w')

        a0=lines[0].split()[-1]
        a1=eval(a0.split('-')[0])
        a2=eval(a0.split('-')[1])
        l3='*'.join(lines[0].split())+'*length='+str(a2-a1+1)+'\n'
        myfile.write(l3)
        myfile.write(lines[1])
        ls=len(lines)/2
        for i in range(1,ls):
            l1=lines[2*i]
            l2=lines[2*i+1]
            b0=l1.split()[-1][:-1]
            b1=eval(b0.split('-')[0])
            b2=eval(b0.split('-')[1])
            c1=min(b1,b2)
            c2=max(b1,b2)
            l1='*'.join(l1.split())+'*length='+str(c2-c1+1)+'\n'
            myfile.write(l1)
            myfile.write(l2)
        myfile.close()

print "Part.4 has been finished successfully!!"

## 5.1 Extend sequences to start witrh the first position of the cds
if os.path.exists(Tem_path+'filling-in')==0:
    os.mkdir(Tem_path+'filling-in')
rootdir1=Tem_path+'/group5/'
rootdir2=Tem_path+'/filling-in/'
files=os.listdir(Tem_path+'/group5/')

for file1 in files:
    lines=open(rootdir1+file1).readlines()
    myfile=open(rootdir2+file1,'w')
    l1=lines[0]
    l1=l1.replace('-','\t')
    l1=l1.replace('_','\t')
    a0=l1.split()[0]
    a0=a0.split('*')[1]
    if eval(a0) !=1:
        for line in lines:
            if '>' in line:
                myfile.write(line)
            else:
                for i in range(eval(a0)-1):
                    myfile.write('+')
                myfile.write(line)
    else:
        for line in lines:
            myfile.write(line)
    myfile.close()


## 5.2. Transpose the aligned sequences
if os.path.exists(Tem_path+'group6')==0:
    os.mkdir(Tem_path+'group6')
rootdir1=Tem_path+'/filling-in/'
rootdir2=Tem_path+'/group6/'
files=os.listdir(Tem_path+'/filling-in/')
for file1 in files:
    lines=open(rootdir1+file1).readlines()
    myfile=open(rootdir2+file1,'w')
    ls=len(lines)/2
    ls2=len(lines[1])
    for i in range(ls):
        l1=lines[2*i][:-1]
        l1='~'.join(l1.split())
        myfile.write(l1+'\t')
    myfile.write('\n')
    for j in range(ls2):
        for l in range(ls):
            l2=lines[2*l+1]
            l2=l2.split()[0]
            l2=l2+'\n'
            myfile.write(l2[j]+'\t')
        myfile.write('\n')
    myfile.close()

## 5.3. Clean the files with transposed sequences
if os.path.exists(Tem_path+'group7')==0:
    os.mkdir(Tem_path+'group7')
rootdir1=Tem_path+'/group6/'
rootdir2=Tem_path+'/group7/'
files=os.listdir(Tem_path+'/group6/')
for file1 in files:
    file2=file1.replace('.txt','.fa')
    lines=open(rootdir1+file1).readlines()
    myfile=open(rootdir2+file2,'w')
    for line in lines:
        if len(line.split())>=2:
            myfile.write(line)
    myfile.close()


## 5.4. Compile start and end points of all exons per gene in a single file
myfile=open(Tem_path+'map','w')
for fname in rGFFnames:
    lines=open(RAW_path+fname).readlines()
    d=[]
    f={}
    i=0
    j=''
    for line in lines:
        if len(line.split())>3:
            if line.split()[2]=='mRNA':
                if i !=0:
                    myfile.write(j+'\t'+ax+'\t||\t'+f[j]+'\n')
                i=i+1
                ax=line.split()[6]
                a0=line.split()[8]
                a1=a0.split(';')[0]
                a2=a1.split('=')[1]
                a3=a2.split('.TAIR')[0]
                j=a3
            elif line.split()[2]=='CDS':
                b0=line.split()[3]
                b1=line.split()[4]
                c=b0+'\t'+b1+'\t|\t'
                if j in d:
                    f[j]=f[j]+c
                else:
                    d.append(j)
                    f[j]=c
myfile.close()
                
            
## 5.5. Add flags for split site positions in the transposed alignment
if os.path.exists(Tem_path+'group8')==0:
    os.mkdir(Tem_path+'group8')
lines=open(Tem_path+'/map').readlines()
rootdir1=Tem_path+'/group7/'
rootdir2=Tem_path+'/group8/'
files=os.listdir(Tem_path+'/group7/')
f={}
d=[]
for line in lines:
    g=[]
    a0=line.split()[0]
    a1=line.split()[3]
    a2=line.split()[4]
    b1=eval(a1)
    b2=eval(a2)
    d.append(a0)
    for j in line.split('|')[2:-1]:
        c0=j.split()[0]
        c1=j.split()[1]
        c2=eval(c0)
        c3=eval(c1)
        c4=abs(c3-c2+1)
        c5=str(c4)
        g.append(c5)
    f[a0]=g

for file1 in files:
    k0=file1.split('_')[0]
    k1=k0.split('.')[0]+'.'+k0.split('.')[1]
    k2=f[k1]
    lines1=open(rootdir1+file1).readlines()
    myfile=open(rootdir2+k1,'w')
    ls=len(lines1[1].split())
    i=0
    k3=[]
    j=0
    for x in k2:
        j=j+eval(x)
        k3.append(j)
    for line in lines1:
        if i in k3:
            myfile.write(line)
            for k in range(ls):
                myfile.write('S\t')
            myfile.write('\n')            
        else:
            myfile.write(line)
        if len(line.split())>=1 and line.split()[0] !='-':
            i=i+1
    myfile.close()

## 5.6. Extract exons into separate files
if os.path.exists(Tem_path+'group9')==0:
    os.mkdir(Tem_path+'group9')
rootdir1=Tem_path+'/group8/'
rootdir2=Tem_path+'/group9/'
files=os.listdir(Tem_path+'/group8/')
for file1 in files:
    i=0
    j=0
    k=0
    lines=open(rootdir1+file1).readlines()
    l1=lines[0]
    for line in lines[1:]:
        if 'S' not in line:
            myfile=open(rootdir2+file1+'.'+str(i+1),'a')
            if j==0:
                myfile.write(l1)
                j=j+1
            myfile.write(line)
            myfile.close()
        else:
            j=0
            i=i+1

## 5.7. Remove exons of insufficient length
if os.path.exists(Tem_path+'group10')==0:
    os.mkdir(Tem_path+'group10')
rootdir1=Tem_path+'/group9/'
rootdir2=Tem_path+'/group10/'
files=os.listdir(Tem_path+'/group9/')
for file1 in files:
    lines=open(rootdir1+file1).readlines()
    d=[]
    for line in lines[1:]:
        if len(line.split())>=1:
            a0=line.split()[0]
            if a0 !='+' and a0 !='-':
                d.append(a0)
    if len(d)>=baits_length:
        myfile=open(rootdir2+file1,'w')
        for line in lines:
            myfile.write(line)
        myfile.close()

print "Part.5 has been finished successfully!!"

## 6.1. Re-transpose files containing the exon sequences to fasta files
if os.path.exists(Tem_path+'group11')==0:
    os.mkdir(Tem_path+'group11')
rootdir1=Tem_path+'/group10/'
rootdir2=Tem_path+'/group11/'
files=os.listdir(Tem_path+'/group10/')
for file1 in files:
    lines=open(rootdir1+file1).readlines()
    myfile=open(rootdir2+file1,'w')
    d=[]
    e=[]
    l1=lines[0]
    a1=len(l1.split())
    for i in l1.split():
        j=i+'\n'
        j=j.replace('~',' ')
        d.append(j)
    for k in range(a1):
        myfile.write(d[k])
        for line in lines[1:]:
            if len(line.split())==a1:
                l=line.split()[k]
                l=l.replace('+','')
                myfile.write(l)
        myfile.write('\n')
    myfile.close()


## 6.2. Remove gaps in exons
if os.path.exists(Tem_path+'group12')==0:
    os.mkdir(Tem_path+'group12')
if os.path.exists(Tem_path+'group13')==0:
    os.mkdir(Tem_path+'group13')

rootdir1=Tem_path+'/group11/'
rootdir2=Tem_path+'/group12/'

rootdir3=Tem_path+'/group13/'

files=os.listdir(Tem_path+'/group11/')
for file1 in files:
    file2=file1+'.fas'
    file3=file1+'.120bp.fas'
    lines=open(rootdir1+file1).readlines()
    myfile=open(rootdir2+file2,'w')
    myfile2=open(rootdir3+file3,'w')    
    ls=len(lines)/2
    for i in range(ls):
        l1=lines[2*i]
        l2=lines[2*i+1]
        l1=l1.replace('*','\t')
        l3=l2.replace('-','')
        ls2=len(l3)
        if ls2>1:
            myfile.write(l1)
            myfile.write(l3)
        if ls2>=(baits_length+1):
            myfile2.write(l1)
            myfile2.write(l3)
    myfile.close()
    myfile2.close()

## 6.3. Extract baits 
if os.path.exists(Tem_path+'group14')==0:
    os.mkdir(Tem_path+'group14')
rootdir1=Tem_path+'/group13/'
rootdir2=Tem_path+'/group14/'
files=os.listdir(Tem_path+'/group13/')
for file1 in files:
    lines=open(rootdir1+file1).readlines()
    ls=len(lines)/2
    a0=file1[:-4]+'_'
    for i in range(1,ls):
        x1=0
        l1=lines[2*i]
        l2=lines[2*i+1]
        a1=l1.split()[0][1:]
        myfile=open(rootdir2+a0+a1+'.fasta','w')
        y=(len(l2)-1)%60
        if y>40:
            x1=1
        x3=(len(l2)-1)/60-1
        for j in range(x3):
            b0=60*(j)
            b1=60*(j+2)
            myfile.write(l1[:-1]+'_'+str(j)+'\n')
            myfile.write(l2[b0:b1]+'\n')
        if x1==1:
            myfile.write(l1[:-1]+'_'+str(j+1)+'_reversed\n')
            myfile.write(l2[-baits_length:])
            
        myfile.close()
        
files2=os.listdir(Tem_path+'/group14/')
if Blast_gap=='1':
    myfile=open(Out_path+'/nogap_baits.combined.fasta','w')
elif Blast_gap=='2':
    myfile=open(Out_path+'/gap_baits.combined.fasta','w')
for file1 in files2:
    a0=file1.split('_')[0]
    lines=open(rootdir2+file1).readlines()
    for line in lines:
        if '>' in line:
            line='>'+a0+'_'+line[1:]
        myfile.write(line)
myfile.close()

## 6.4. Combine exon sequences into single files per species
rootdir=Tem_path+'group13/'
for fname in sFNAnames:
    fname1=fname[:4]+'.fasta'
    myfile=open(Tem_path+fname1,'w')
    files=os.listdir(Tem_path+'group13/')
    for file1 in files:
        a=file1[:-9]
        lines=open(rootdir+file1).readlines()
        ls=len(lines)/2
        for i in range(ls):
            l1=lines[2*i]
            l3='>'+a+'_'+l1[1:]
            l2=lines[2*i+1]
            a0=l1[1:5]
            if a0 in fname1:
                myfile.write(l3)
                myfile.write(l2)
    myfile.close()


print "Part.6 has been finished successfully!!"

## 7.1. Remove genes with too few baits in teh best-quality focal species
if len(sufficient)>0:
    if Blast_gap=='1':
        lines=open(Out_path+'nogap_baits.combined.fasta').readlines()
        myfile=open(Out_path+'nogap_sorted.result.fa','w')
    elif Blast_gap=='2':
        lines=open(Out_path+'gap_baits.combined.fasta').readlines()
        myfile=open(Out_path+'gap_sorted.result.fa','w')
    f={}
    d=[]
    e=[]
    for line in lines:
        x0=0
        for x1 in sufficient:
            x1=x1.split('.')[0]
            if x1 in line:
                x0=1            
            if x0==1:
                a1=line.split()[3]
                if a1 not in d:
                    d.append(a1)
                    f[a1]=1
                else:
                    f[a1]=f[a1]+1
    for i in d:
        j=f[i]
        if j>=4:
            e.append(i)
    ls=len(lines)/2
    for k in range(ls):
        l1=lines[2*k]
        l2=lines[2*k+1]
        c=l1.split()[3]
        if c in e:
            myfile.write(l1)
            myfile.write(l2)
    myfile.close()

## Wait for CD-HIT-EST


