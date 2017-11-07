lines=open('Mguttatus.arabidopsis.1-p').readlines()
myfile=open('Mguttatus.arabidopsis.single.gene.list','w')
c=[]
d=[]
e=[]
f={}
g=[]
lines=sorted(lines)
for line in lines:
    ax=line.split()[-2]
    ax=ax.replace(',','.')
    ax=float(ax)
    ay=line.split()[2]
    ay=float(ay)
    if  ay>=25:
        a0=line.split()[0]
        a1=a0.split('.')[0]+'.'+a0.split('.')[1]
        a2=a0.split('.')[0]+'.'+a0.split('.')[1]+a0.split('.')[2]
        a3=line.split()[1]
        a4=a1+'\t'+a3
        if a3 not in c:
            f[a3]=1
            c.append(a3)
            d.append(a4)
        elif a4 not in d:
            f[a3]=f[a3]+1
for line in lines:
    ax=line.split()[-2]
    ax=ax.replace(',','.')
    ax=float(ax)
    ay=line.split()[2]
    ay=float(ay)
    if ay>=25:
        a5=line.split()[0]
        a6=line.split()[1]
        if f[a6]==1:
            a7=a5.split('.')[0]+'.'+a5.split('.')[1]
            a8=a5.split('.')[0]+'.'+a5.split('.')[1]+'.'+a5.split('.')[2]
            if a7 not in g:
                e.append(a5)
                g.append(a7)
for i in e:
    myfile.write(i+'\n')
myfile.close()
lines2=open('Mguttatus_256_v2.0.protein.fasta').readlines()
myfile=open('Mguttatus.arabidopsis.single.gene.list.fa','w')
x=0
for line in lines2:
    if '>' in line:
        x=0
        b0=line.split()[2]
        b1=b0.split('=')[1]
        b1=b1+'.p'
        if b1 in e:
            myfile.write(line)
            x=1
    elif x==1:
        myfile.write(line)
myfile.close()
