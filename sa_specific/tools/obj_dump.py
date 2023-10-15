
# [ ] support classes with excluded_fields.

import truthdb, spinobj, multimaster, spinerror, sys, os, string, pwd, re, threading

def usage():
  sys.stderr.write( 
"""Usage:  %s [-w <width>] [-f] [-l] [-i <file>] <obj_class> <obj_id> 
           [<obj_class2> <obj_id2> ...]

        %s -h

  [-w <width>]
      Render table to width <width>.  Default is to take the width of the tty
      on stderr (fd 2).  If stderr is not a tty, then a width of 80 is assumed.

  [-f]
      Draw a full table with borders around each cell.

  [-l]
      Only query the local core's database.

  [-i <file>]
      Read entries from file given by <file>.  If <file> is "-", then reads
      from standard input.  Each line of <file> is expected to be of the form
      "<obj_class> <obj_id>".

  <obj_class> <obj_id>
      Class name and object id to be queried.

  -h
      Shows this usage info.

Example:

  > ./sql Device 120501
""" % ((sys.argv[0],)*2))
  sys.exit(1)

if ( len(sys.argv) == 1 ):
  usage()

import string, struct, termios, fcntl, tty
# hack for python 1.5.x version of termios that seems to lack TIOCGWINSZ.
if ( not hasattr(termios,"TIOCGWINSZ") ):
  if ( string.find( sys.platform, "linux" ) > -1 ): termios.TIOCGWINSZ=21523
  elif ( string.find( sys.platform, "freebsd" ) > -1 ): termios.TIOCGWINSZ=1074295912
  elif ( string.find( sys.platform, "solaris" ) > -1 ): termios.TIOCGWINSZ=21608

def ioctl_GWINSZ( fo ):
  size = (25, 80)
  if ( fo.isatty() ):
    try:
      size = struct.unpack('hh', fcntl.ioctl(fo.fileno(), termios.TIOCGWINSZ, 'abcd'))
    except:
      pass
  return size

import types, operator, cStringIO
# "Outer" transpose:
# ((1,2),(3,4,5)) -> ((1,3),(2,4),(None,5))
def otranspose(lstRows,empty=None):
  lstRet = []
  lstRowLens = map(len,lstRows)
  nMaxRowLen = max(lstRowLens)
  nCurCol = 0
  def item(lst, nCurItem, empty):
    if nCurItem < len(lst): return lst[nCurItem]
    else: return empty
  while nCurCol < nMaxRowLen:
    lstRet.append(tuple(map(lambda lstRow,e=empty,n=nCurCol,item=item:item(lstRow,n,e), lstRows)))
    nCurCol = nCurCol + 1
  return lstRet

# inspired by Mike Brown's:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
def fmtcols(lstCols, nWidth=80, bHeader=0, sHeaderChar='-', sDelim=' | ', 
    sNlChar='\n', fnJustify='left', bSepRows=0, sSepChar='-', sPrefix='', 
    sPostfix='', fnFmt=None, fnWrap=None):
  """Formats tabular data for text printing with a focus on horizontal width
optimization.
  lstCols: A sequence of columns.  Each column is a sequence of strings.
  nWidth: Width of text to render the table to.
  bHeader: Will render a seperate under the first row if set.
  sHeaderChar: Character to use to build the header seperator.
  sDelim: Character to use for horizontal seperation between cells.
  sNlChar: String to use to render newlines.
  fnJustify: (lambda r,c) Function that returns one of 'left', 'right', or 
    'center' based on zero-indexed cell coordinates <r> and <c> for row and
    column respectively.  If set to a string value, then a function will be
    used that always returns the given string value.
  bSepRows: Will render a seperator between every row if set.
  sSepChar: Character to use to render the seperator.
  sPrefix: String to use on the left side of every rendered row.
  sPostfix: String to use on the right side of every rendered row.
  fnFmt: (lambda r,c,pcv) Function that can be used to wrap the physical cell
    value <prv> at the row/column coordinates given by <r>, <c> with extra
    control codes to implement formatting.
  fnWrap: (lambda lcv,w) Function that can be used to implement custom wrapping
    logic.  <lcv> will be a list resulting from spliting the given cell value 
    using <sNlChar>.  The function must insure that no elements of this list 
    are longer than <w> characters.
"""
  # Some private functions.
  def _center(s,w):
    w = int(w-len(s))
    if ( w < 1 ): return s
    p = ' ' * w
    return p[:w/2] + s + p[w/2:]

  def _rjust(s,w):
    w = int(w-len(s))
    if ( w < 1 ): return s
    return (' ' * w) + s

  def _ljust(s,w):
    w = int(w-len(s))
    if ( w < 1 ): return s
    return s + (' ' * w)

  mapJustifyFns = {'center':_center, 'right':_rjust, 'left':_ljust}

  def _defWrap(lcv,w):
    lcv_ret = []
    for pcv in lcv:
      while (len(pcv)>w):
        lcv_ret.append(pcv[:w])
        pcv = pcv[w:]
      if (pcv): lcv_ret.append(pcv)
    return lcv_ret

  if (type(fnJustify) == types.StringType):
    fnJustify = lambda r,c,v=fnJustify:v

  if (not fnWrap): fnWrap = _defWrap

  if (not fnFmt): fnFmt = lambda r,c,pcv: pcv

  if (not lstCols): return ''

  nNumCols = len(lstCols)

  # Split each cell into physical cells by newline.
  lstCols = map(lambda col,nl=sNlChar:map(lambda item,nl=nl:string.split(item,nl), col), lstCols)

  # Embed the maximum natural length of each column.
  lstCols = map(lambda col:[col, max(map(lambda lc:max(map(lambda pc:len(pc),lc)),col))], lstCols)

  # Create a copy of the list of columns to work with
  lstWorkCols = map(lambda col:col, lstCols)

  # Calculate the avialable width for the columns.
  nNonColWidth = len(sPrefix) + ((len(lstWorkCols)-1) * len(sDelim)) + len(sPostfix)
  nCurWidth = nWidth - nNonColWidth

  # Optimize the column widths to fit.
  while (lstWorkCols):
    nCurCols = len(lstWorkCols)
    fAvgWidth = float(nCurWidth)/nCurCols
    lstPoppedCols = filter(lambda col,f=fAvgWidth:col[1]<=f, lstWorkCols)
    lstWorkCols = filter(lambda col,f=fAvgWidth:col[1]>f, lstWorkCols)
    if (lstPoppedCols):
      nCurWidth = nCurWidth - reduce(lambda a,b:(None,a[1]+b[1]), lstPoppedCols)[1]
    else:
      col = lstWorkCols.pop()
      nAvgWidth = max(1,int(fAvgWidth))
      col[1] = nAvgWidth
      # Use the user specified wraper function to wrap logical cells of columns
      # that need horizontal squeezing
      col[0] = map(lambda lcv,w=nAvgWidth,fn=fnWrap:fn(lcv,w), col[0])
      nCurWidth = nCurWidth - nAvgWidth

  # Extract column widths.
  lstColWidths = map(lambda col:col[1], lstCols)
  lstCols = map(lambda col:col[0], lstCols)

  # Calculate the actual width of the table after formating.
  nWidth = reduce(operator.add, lstColWidths) + nNonColWidth

  # Transpose the list of columns into a list of rows.
  lstRows = otranspose(lstCols)

  # Extend the list of physical cells for each row so that they are all the same.
  lstRows = map(lambda lrow:otranspose(lrow,''), lstRows)

  # Create a string buffer.
  sb = cStringIO.StringIO()

  if (bHeader):
    sHeader = sHeaderChar*nWidth + '\n'

  if (bSepRows):
    sRowSep = sSepChar*nWidth + '\n'
    sb.write(sRowSep)

  # Render the table.
  nCurLRow = 0
  nRows = len(lstRows)
  while (nCurLRow < nRows):
    for prow in lstRows[nCurLRow]:
      nCurCol = 0
      sb.write(sPrefix)
      while (nCurCol < nNumCols):
        pcell = mapJustifyFns[fnJustify(nCurLRow, nCurCol)](prow[nCurCol], lstColWidths[nCurCol])
        sb.write(fnFmt(nCurLRow, nCurCol, pcell))
        if (nCurCol < (nNumCols - 1)): sb.write(sDelim)
        nCurCol = nCurCol + 1
      sb.write(sPostfix)
      sb.write(sNlChar)
    if (bHeader and (nCurLRow == 0)): sb.write(sHeader)
    elif (bSepRows): sb.write(sRowSep)
    nCurLRow = nCurLRow + 1

  # Return the rendered table.
  return sb.getvalue()

method = "table_checker"
user = pwd.getpwuid(os.getuid())[0]

def loadObjThread(dc, sql, obj_ids, mapObjs):
  try:
    db = multimaster.getDB( method, user, dc.getDBName() )
  except spinerror.DBConnectError, e:
    sys.stderr.write("\n%s: %s: %s\n" % (sys.argv[0], dc, e))
    return
  cur = db.getCursor()
  cur.execute(sql, obj_ids)
  rs = cur.fetchall()
  sys.stdout.write(" %s" % dc.getID())
  sys.stdout.flush()
  dc_id = dc.getID()
  mapObjs[dc_id] = {}

  # Inject results into result map.
  for r in rs:
    if ( len(r) > 0):
      mapObjs[dc_id][r[0]] = r[1:]

def rawToStr(val):
  typVal = type(val)
  if ( typVal == types.FloatType ):
    if ( (val - int(val)) < 1 ):
      return str(int(val))
    else:
      return str(val)
  elif ( typVal == types.NoneType ):
    return '<null>'
  elif ( typVal == types.LongType ):
    return str(val)[:-1]
  else:
    return str(val)

g_bUseVT = sys.stdout.isatty()
def _vt_attr(s,attrs):
  if (g_bUseVT):
    return "\x1b[%sm%s\x1b[m" % (string.join(map(lambda a:str(a),attrs), ';'), s)
  else: return s

def obj_dump(obj_cls_name, obj_ids, bLocalOnly):
  db = truthdb.DB()

  # Get the object class keys.
  obj_cls = spinobj.getObjectClass(obj_cls_name)
  # In case there are some excluded fields.
  if ( hasattr(obj_cls, "exclude_fields") ):
    obj_cls.exclude_fields = []
  obj_cls = obj_cls(db)

  # In case we are running on a pre-7.0 spin without a splitCompoundID method.
  if ( not hasattr(obj_cls, "splitCompoundID") ):
    obj_cls.splitCompoundID = lambda id: string.split(id,'-')
  # In case we are running on a pre-7.0 spin without a compound_id_delimiter.
  if (not hasattr( obj_cls, "compound_id_delimiter" ) ):
    obj_cls.compound_id_delimiter = '-'

  # Calculate the sql query to load the objects.
  cls_fields = map(lambda f:f.name, obj_cls.getFields())
  id_fields = map(lambda f:f.name, obj_cls.getIDFields())
  select_columns = string.join(cls_fields, ',')
  sql_id = "to_char(%s)" % string.join(id_fields, "||'" + obj_cls.compound_id_delimiter + "'||")
  in_clause = "(%s)" % string.join(map(lambda i:":p%d" % i, range(len(obj_ids))),',')
  sql = "select %s, %s from %s where %s in %s" % (sql_id, select_columns, obj_cls._table.name, sql_id, in_clause)

  dc_ids = [db.getDCID()]
  all_dcs = multimaster.getAllDCs( method, user )
  if ( not bLocalOnly ):
    dc_ids = all_dcs.keys()

  sys.stdout.write("Loading %d object(s) from DC:" % len(obj_ids))
  sys.stdout.flush()
  dc_ids.sort()
  lstLoadObjThreads = []
  mapAllObjs = {}
  for dc_id in dc_ids:
    dc = all_dcs[dc_id]
    lot = threading.Thread(target=loadObjThread, args=(dc,sql,obj_ids,mapAllObjs))
    lot.start()
    lstLoadObjThreads.append(lot)

  for lot in lstLoadObjThreads:
    lot.join()

  sys.stdout.write("\n")

  if ( len(mapAllObjs) != len(dc_ids) ):
    sys.stderr.write("%s: failure to load object from some datacenters.\n" % sys.argv[0])
    sys.exit(1)

  for obj_id in obj_ids:
    mapObjs = {}
    for dc_id in dc_ids:
      if ( mapAllObjs[dc_id].has_key(obj_id) ):
        mapObjs[dc_id] = mapAllObjs[dc_id][obj_id]
      else:
        mapObjs[dc_id] = None
      
    lstRH = []
    lstCH = []
    def Fmt(r,c,pcv,lstRH,lstCH):
      if (g_bUseVT):
        if ((r in lstRH) or (c in lstCH)):
          return _vt_attr(pcv,(1,31))
        elif (float(r)/2 == r/2):
#        elif ((r==0) or (c==0)):
          return _vt_attr(pcv,(1,))
        else:
          return pcv
      else: return pcv
    # Create a closure.
    fnFmt = lambda r,c,pcv,rh=lstRH,ch=lstCH,Fmt=Fmt:Fmt(r,c,pcv,rh,ch)

    # Detect which columns to highlight as missing the object in question.
    nCurCol = 0
    while nCurCol < len(dc_ids):
      dc_id = dc_ids[nCurCol]
      if (mapObjs[dc_id] == None):
        lstCH.append(nCurCol+1)
      nCurCol = nCurCol +1

    # Detect which rows to highlight as having differing data.
    if (len(lstCH) == 0):
      nCurRow = 0
      while nCurRow < len(cls_fields):
        val = mapObjs[dc_ids[0]][nCurRow]
        for dc_id in dc_ids[1:]:
          if (val != mapObjs[dc_id][nCurRow]):
            lstRH.append(nCurRow+1)
            break
        nCurRow = nCurRow + 1

    # Collect results into a final table.
    lstCols = [[''] + cls_fields]

    # Collect data into list of columns.
    for dc_id in dc_ids:
      # Map over each result field and convert to string.
      mapObj = mapObjs[dc_id]
      lstVals = ["%d %s" % (int(dc_id), all_dcs[dc_id]['display_name'])]
      if ( mapObj ):
        lstVals.extend(map(lambda v:rawToStr(v),mapObjs[dc_id]))
      else:
        lstVals.extend(["not found",] * len(cls_fields))
      lstCols.append(lstVals)

    # Prepend a '*' char to the field names.
    nCurRow = 0
    while (nCurRow < len(lstCols[0])):
      if (nCurRow in lstRH):
        lstCols[0][nCurRow] = '*' + lstCols[0][nCurRow]
      nCurRow = nCurRow + 1

    # Prepend a '*' char to the column headers.
    nCurCol = 0
    while (nCurCol < len(lstCols)):
      if (nCurCol in lstCH):
        lstCols[nCurCol][0] = '*' + lstCols[nCurCol][0]
      nCurCol = nCurCol + 1
    
    # Print out table for the current object.
    sys.stdout.write(_vt_attr("%s %s:\n" % (obj_cls_name, obj_id),(1,)))
    if ( bFullTable ):
      table = fmtcols(lstCols, fnJustify=fnJustify, bSepRows=1, sPrefix='| ', sPostfix=' |', nWidth=nWidth, fnFmt=fnFmt) + '\n'
    else:
      table = fmtcols(lstCols, fnJustify=fnJustify, bHeader=1, nWidth=nWidth, fnFmt=fnFmt) + '\n'

    sys.stdout.write(table)

def query_class(sClsQuery):
  sClsQuery = string.lower(sClsQuery)
  lstClasses = spinobj.getClasses().values()
  if ( sClsQuery ):
    lstClasses = filter(lambda cls:(string.find(string.lower(cls['name']),sClsQuery) > 0) or (string.find(string.lower(cls['table_name']),sClsQuery) > 0), lstClasses)
  print map(lambda cls:(cls['name'], cls['table_name']), lstClasses)

def shift(lst):
  if lst:
    ret = lst[0]
    del lst[0]
    return ret
  else:
    return None

if __name__ == '__main__':
  # Set some defaults.
  nWidth = ioctl_GWINSZ(sys.stderr)[1]
  bFullTable = 0
  bLocalOnly = 0
  sInFile = None
  fnJustify='left'

  # Make a copy of the arguments list.
  lstArgv = map(lambda arg:arg, sys.argv[1:])

  # Consume initial decoration options.
  while (lstArgv[0] in ['-w', '-f', '-l', '-i']):
    arg = shift(lstArgv)
    if ( arg == '-w' ):
      nWidth = int(shift(lstArgv))
    elif ( arg == '-f' ):
      bFullTable = 1
    elif (arg == '-l'):
      bLocalOnly = 1
    elif (arg == '-i'):
      sInFile = shift(lstArgv)
    else:
      usage()
    if (len(lstArgv) == 0): break

  if (len(lstArgv) and lstArgv[0] == '-h'):
    usage()
  if (len(lstArgv) and lstArgv[0] == '-q'):
    shift(lstArgv)
    sClsQuery = ""
    if ( len(lstArgv) > 0 ):
      sClsQuery = lstArgv[0]
    query_class(sClsQuery)
  else:
    mapObjIds = {}

    # Collect objects from the command line.
    while lstArgv:
      obj_cls_name = shift(lstArgv)
      if (not mapObjIds.has_key(obj_cls_name)): mapObjIds[obj_cls_name] = []
      mapObjIds[obj_cls_name].append(shift(lstArgv))

    # Collect objects from optionally specified file.
    if (sInFile):
      if (sInFile == "-"):
        f = sys.stdin
      else:
        f = open(sInFile)
      for sObj in f.readlines():
        sObj = string.replace(string.replace(sObj, "\n", ""), "\r", "")
        sObj = string.strip(sObj)
        try:
          (obj_cls_name, obj_id) = string.split(sObj, " ")
          if (not mapObjIds.has_key(obj_cls_name)): mapObjIds[obj_cls_name] = []
          mapObjIds[obj_cls_name].append(obj_id)
        except:
          sys.stderr.write("%s: %s: %s: Warning: does not match \"<obj_class> <obj_id>\" pattern.\n" % (sys.argv[0], sInFile, sObj))

    # Itterate through each class specified and dump the objects out.
    for obj_cls_name in mapObjIds.keys():
      obj_ids = mapObjIds[obj_cls_name]
      try:
        obj_dump(obj_cls_name, obj_ids, bLocalOnly)
      except IOError, e:
        # User disconnected, ignore
        pass
