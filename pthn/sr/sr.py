import os
import sys
import datefinder

os.system('pdf2txt.py -o ' + sys.argv[1] + ' ' + sys.argv[1] + '.pdf')

lines_seen = set() 
outfile = open('sr', "w")
for line in open(sys.argv[1], "r"):
  if line not in lines_seen: # not a duplicate
    outfile.write(line)
    lines_seen.add(line)
outfile.close()

for line in open('sr', "r"):
    matches = datefinder.find_dates(line)
    for match in matches:
      print(match)
