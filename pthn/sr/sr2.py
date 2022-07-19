import os
import sys
import datefinder

os.system('pdf2txt.py -o ' + sys.argv[1] + ' ' + sys.argv[1] + '.pdf')

f = open(sys.argv[1])
s = f.read()
m = s.split('Description:')
m.reverse()
res = []
lines_seen = set()
outfile = open('thisone', "w")
[res.append(x) for x in m if x not in res]
with open('sr.txt','w') as sr:
    for element in m:
        sr.write('%s\n' % element)

for line in open('sr.txt','r'):
    if line not in lines_seen:
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

