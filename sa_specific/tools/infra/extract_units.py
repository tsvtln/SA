import sys,gzip,string,cPickle,types
import xml.etree.ElementTree as etree

def err(msg):
  sys.stderr.write(msg)
  sys.stderr.flush()

def shift(l):
  r = l[0]
  del l[0]
  return r

root = None
ai = None
ar = None

argv = sys.argv[1:]
while argv:
  cur_arg = shift(argv)
  if ( cur_arg == "-rf" ):
    repo_file = shift(argv)
    err("loading repo data from %s\n" % repo_file)
    if ( repo_file[-3:] == ".gz" ):
      tree = etree.parse(gzip.open(repo_file))
    else:
      tree = etree.parse(open(repo_file))
    root = tree.getroot()
  elif ( cur_arg == "-ai" ):
    ai_file = shift(argv)
    err("loading analysis input data set\n")
    ai = eval(open(ai_file).read())
  elif ( cur_arg == "-ar" ):
    ar_file = shift(argv)
  else:
    err("%s: Unknown argument, ignoring\n" % cur_arg)

# rpm -qa --queryformat "%{name}-%{version}-%{release}.%{arch}\n"
def extract_units(root):
  m = {}
  for pkg in root:
    uid = "uid"
    n = "<name>"
    v = "<version>"
    e = "<epoch>"
    r = "<release>"
    a = "<arch>"
    for el in pkg:
      if ( el.tag == '{http://linux.duke.edu/metadata/common}name' ):
        n = el.text
      elif ( el.tag == '{http://linux.duke.edu/metadata/common}arch' ):
        a = el.text
      elif ( el.tag == '{http://linux.duke.edu/metadata/common}version' ):
        v = el.attrib['ver']
        r = el.attrib['rel']
      elif ( el.tag == '{http://linux.duke.edu/metadata/common}location' ):
        uid = string.strip(string.split(el.attrib['href'],'=')[1])
    m[uid] = "%s-%s-%s.%s" % (n,v,r,a)
  return m

def str_id(id):
  if ( type(id) != types.StringType ):
    id = "%d" % id
  return id

def resolve_ai(ai, us):
  for i in ai:
    uid = None
    if ( i[0] in ("INSTALLONLY", "ALLOW_DOWNGRADE") ):
      uid = str_id(i[1])
    elif ( i[0] == "+" ):
      uid = str_id(i[2])
    if ( uid is not None ):
      i.append(us.get(uid,"*unit not found*"))
      
def resolve_ar(ar,us):
  for i in ar:
    uid = str_id(i[1])
    if ( us.has_key(uid) ):
      i.append(us[uid])

err("extracting unit names from repo data\n")
us = extract_units(root)

if ( ar is not None ):
  err("resolving analyze_results into unit names\n")
  resolve_ar(ar,us)

  err("emitting resolved analyze_results\n")
  for i in ar:
    sys.stdout.write(str(i) + '\n')
    sys.stdout.flush()

if ( ai is not None ):
  err("resolving analyze input data set into unit names\n")
  resolve_ai(ai,us)

  err("emitting resolved analyze input\n")
  for i in ai:
    sys.stdout.write("%s\n" % str(i))
    sys.stdout.flush()
