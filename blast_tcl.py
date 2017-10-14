import os,os.path
import platform
from multiprocessing import cpu_count

CPU_n1=cpu_count()
CPU_n2=str(max(1,CPU_n1))

##platform##
plat=platform.platform()
if "Windows" in plat:
    Sys_ver = 'W'
elif "Linux" in plat:
    Sys_ver = 'L'

##get config file##

path = os.path.abspath(os.curdir)
config = path.replace('\\','/')+'/config.ini'

##check if config file exists##
CRC0=os.path.exists(config)

if os.path.exists(config)== 0:
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

##read config file##
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
            Blast_path=line.replace('\\','/').split('=')[1].strip()+'/'
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
        elif 'host_name' in line:
            CRC0+=1
            CRC2+=1
            a0=line.split('=')[0].strip()
            a1=line.split('=')[2].strip()
            host2[a0]=a1
            if a1 !='NAN':
                host1[a0]='1'
        elif 'sufficient_data' in line:
            a0=line.split('=')[1].strip()
            if a0!='NAN':
                sufficient.append(a0)

##creat a new folder for output##
if os.path.exists(path+'/blast_tcl_out') == 0:
    os.mkdir(path + "/blast_tcl_out")
out_path = path + "/blast_tcl_out/"

##do blast##
database_path = RAW_path+ rFAAnames[0]

if Blast_gap == "1":
    gap = "F"
elif Blast_gap == "2":
    gap = "T"

for qname in sFNAnames:
        if Sys_ver == 'L':
            if gap == "F":

                val = os.system('formatdb -i ' + database_path + ' -p T')
                val = os.system('blastall -p blastx -d ' + database_path + ' -i ' + RAW_path + qname + ' -e 1e-10 -o' + out_path + qname.split(".")[0] + "_ungap.out" + ' -F "m S" -v 24 -b 24 -g ' + gap + ' -a 1')
            elif gap == "T":

                val = os.system('formatdb -i ' + database_path + ' -p T')
                val = os.system('blastall -p blastx -d ' + database_path + ' -i ' + RAW_path + qname + ' -e 1e-10 -o' + out_path + qname.split(".")[0] + "_gap.out" + ' -F "m S" -v 24 -b 24 -g ' + gap + ' -a 1')

        else:

            if gap == "F":
                val = os.system(Blast_path + 'formatdb.exe -i ' + database_path + ' -p T')
                print(Blast_path + 'formatdb.exe -i ' + database_path + ' -p T')
                val = os.system(Blast_path + 'blastall.exe -p blastx -d ' + database_path + ' -i ' + RAW_path + qname + ' -e 1e-10 -o ' + out_path + qname.split(".")[0] + "_ungap.out" + ' -F "m S" -v 24 -b 24 -g ' + gap + ' -a 1')
                print(Blast_path + 'blastall.exe -p blastx -d ' + database_path + ' -i ' + RAW_path + qname + ' -e 1e-10 -o ' + out_path + qname.split(".")[0] + "_ungap.out" + ' -F "m S" -v 24 -b 24 -g ' + gap + ' -a 1')
            elif gap == "T":
                val = os.system(Blast_path + 'formatdb.exe -i ' + database_path + ' -p T')
                val = os.system(Blast_path + 'blastall.exe -p blastx -d ' + database_path + ' -i ' + RAW_path + qname + ' -e 1e-10 -o' + out_path + qname.split(".")[0] + "_gap.out" + ' -F "m S" -v 24 -b 24 -g ' + gap + ' -a 1')


##do tcl##

for qname in sFNAnames:
    if gap == "F":
        os.system("tclsh tcl_blast_parser_123_V047.tcl " + out_path + qname.split(".")[0] + "_ungap.out" + " " + out_path + qname.split(".")[0] + "_ungap.out" + " 20 40 100 MATRIX")
    else:
        os.system("tclsh tcl_blast_parser_123_V047.tcl " + out_path + qname.split(".")[0] + "_gap.out" + " " + out_path + qname.split(".")[0] + "_gap.out" + " 20 40 100 MATRIX")
