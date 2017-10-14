lines=open('Mguttatus.arabidopsis').readlines()
myfile=open('Mguttatus.arabidopsis.1-p','w')
for line in lines:
    a0=line.split()[0]
    if '.1.p' in a0:
        myfile.write(line)
myfile.close()
