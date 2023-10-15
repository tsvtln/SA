#!/opt/opsware/bin/python

import sys, string

MAXARGS = 255

def parseInfile(objTxtFile):
  objectClassHash={}
  inFile = open(objTxtFile,'r')
  line=inFile.readline()
  while line:
    line=string.strip(line)
    (objectClass,objectId)=string.split(line,' ')
    if not objectClassHash.has_key(objectClass):
      objectClassHash[objectClass]=[]
    objectClassHash[objectClass].append(objectId)
    line=inFile.readline()

  inFile.close()
  return objectClassHash

def writeScriptFile(scriptFile,objectClassHash):
  outFile = open(scriptFile,'w')
  outFile.write('#!/bin/sh\n')
  outFile.write('# I am written by mk_rechk.py\n')
  outFile.write('# which was written by dj@opsware.com\n')
  outFile.write('\n')
  outFile.write('date\n')
  ocKeys=objectClassHash.keys()
#  ocKeys.sort()
  for key in ocKeys:
    idArray=objectClassHash[key]
    while idArray:
      smallIdArray=idArray[:MAXARGS]
      idArray=idArray[MAXARGS:]
      idArgs=string.join(smallIdArray)
      outFile.write('/opt/opsware/bin/python ./table_checker.py -c %s --simple %s\n' % (key, idArgs))
      outFile.write('date\n')

  outFile.close()

def main(objTxtFile,scriptFile):
  objectClassHash=parseInfile(objTxtFile)
  writeScriptFile(scriptFile,objectClassHash)

if __name__ == '__main__':
  if len(sys.argv) == 3:
    objTxtFile = sys.argv[1]
    scriptFile = sys.argv[2]
  else:
    print 'Usage: %s <objTxtFile> <scriptFile>' % sys.argv[0]
    sys.exit(1)

  main(objTxtFile,scriptFile)
