f2 = open('ITAG_nohit','r')
f1 = open('ITAG2.4_proteins.fasta','r')
f3 = open('ITAG_sorted','w')

AI_DICT = {}
for line in f2:
    AI_DICT[line[:-1]] = 1

skip = 0
for line in f1:
    if line[0] == '>':
        _splitline = line.split('|')
        accessorIDWithArrow = _splitline[0]
        accessorID = accessorIDWithArrow[1:-1]
        # print accessorID
        if accessorID in AI_DICT:
            f3.write(line)
            skip = 0
        else:
            skip = 1
    else:
        if not skip:
            f3.write(line)

f1.close()
f2.close()
f3.close()
