import string,cStringIO,operator,types

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

def _stringify(data):
  """Helper function to convert columns or rows given by <data> to all strings.
"""
  data = data[:]
  i = 0
  while i < len(data):
    l = []
    for c in data[i]:
      if (type(c) == types.LongType):
        l.append( "%d" % c )
      else:
        l.append( str(c) )
    data[i] = tuple(l)
    i = i + 1
  return data

# inspired by:
# http://code.activestate.com/recipes/577615-table-indentation/
def fmtcols(lstCols, n_width=80, b_header=0, sHeaderChar='-', col_sep=' | ', 
    sNlChar='\n', fnJustify='left', bSepRows=0, sSepChar='-', sPrefix='', 
    sPostfix='', fn_fmt=None, fnWrap=None):
  """Formats tabular data for text printing with a focus on horizontal width
optimization.
  lstCols: A sequence of columns.  Each column is a sequence of strings.  If
    any column entries are not strings, they will be converted to strings.
  n_width: Width of text to render the table to.
  b_header: Will render a seperate under the first row if set.
  sHeaderChar: Character to use to build the header seperator.
  col_sep: Character to use for horizontal seperation between cells.
  sNlChar: String to use to render newlines.
  fnJustify: (lambda r,c) Function that returns one of 'left', 'right', or 
    'center' based on zero-indexed cell coordinates <r> and <c> for row and
    column respectively.  If set to a string value, then a function will be
    used that always returns the given string value.
  bSepRows: Will render a seperator between every row if set.
  sSepChar: Character to use to render the seperator.
  sPrefix: String to use on the left side of every rendered row.
  sPostfix: String to use on the right side of every rendered row.
  fn_fmt: (lambda r,c,pcv) Function that can be used to wrap the physical cell
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

  lstCols = _stringify(lstCols)

  if (type(fnJustify) == types.StringType):
    fnJustify = lambda r,c,v=fnJustify:v

  if (not fnWrap): fnWrap = _defWrap

  if (not fn_fmt): fn_fmt = lambda r,c,pcv: pcv

  if (not lstCols): return ''

  nNumCols = len(lstCols)

  # Split each cell into physical cells by newline.
  lstCols = map(lambda col,nl=sNlChar:map(lambda item,nl=nl:string.split(item,nl), col), lstCols)

  # Embed the maximum natural length of each column.
  lstCols = map(lambda col:[col, max(map(lambda lc:max(map(lambda pc:len(pc),lc)),col))], lstCols)

  # Create a copy of the list of columns to work with
  lstWorkCols = map(lambda col:col, lstCols)

  # Calculate the avialable width for the columns.
  nNonColWidth = len(sPrefix) + ((len(lstWorkCols)-1) * len(col_sep)) + len(sPostfix)
  nCurWidth = n_width - nNonColWidth

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
  n_width = reduce(operator.add, lstColWidths) + nNonColWidth

  # Transpose the list of columns into a list of rows.
  lstRows = otranspose(lstCols)

  # Extend the list of physical cells for each row so that they are all the same.
  lstRows = map(lambda lrow:otranspose(lrow,''), lstRows)

  # Create a string buffer.
  sb = cStringIO.StringIO()

  if (b_header):
    sHeader = sHeaderChar*n_width + '\n'

  if (bSepRows):
    sRowSep = sSepChar*n_width + '\n'
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
        sb.write(fn_fmt(nCurLRow, nCurCol, pcell))
        if (nCurCol < (nNumCols - 1)): sb.write(col_sep)
        nCurCol = nCurCol + 1
      sb.write(sPostfix)
      sb.write(sNlChar)
    if (b_header and (nCurLRow == 0)): sb.write(sHeader)
    elif (bSepRows): sb.write(sRowSep)
    nCurLRow = nCurLRow + 1

  # Return the rendered table.
  return sb.getvalue()

# Adapter for formatting rows:
def fmtrows(rows, **kwargs):
#  return fmtcols(otranspose(rows), **kwargs)
  return apply(fmtcols, (otranspose(rows),), kwargs)

def renderCols(rows, hasHeader=0, headerChar='-', delim=' | ', justify='left',
           sepRows=0, prefix='', postfix='', wrapfunc=lambda x:x):
    """Indents a table by column.
       - rows: A sequence of sequences of items, one sequence per row.
       - hasHeader: True if the first row consists of the columns' names.
       - headerChar: Character to be used for the row separator line
         (if hasHeader==True or sepRows==True).
       - delim: The column delimiter.
       - justify: Determines how are data justified in their column. 
         Valid values are 'left','right' and 'center'.
       - sepRows: True if rows are to be separated by a line
         of 'headerChar's.
       - prefix: A string prepended to each printed row.
       - postfix: A string appended to each printed row.
       - wrapfunc: A function f(text) for wrapping text; each element in
         the table is first wrapped by this function."""
    def _zip(*args):
        return apply(map, (None,) + args)

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

    # closure for breaking logical rows to physical, using wrapfunc
    def rowWrapper(row,wrapfunc):
        newRows = map(lambda item,wf=wrapfunc:string.split(wf(item),'\n'), row)
        return map(lambda item:map(lambda substr,item=item:substr or '', item), apply(map, (None,) + tuple(newRows)))

    # break each logical row into one or more physical ones
    logicalRows = map(lambda row,rw=rowWrapper,wf=wrapfunc:rw(row,wf), rows)
    print repr(logicalRows)
    # columns of physical rows
    columns = apply(map, (None,) + tuple(reduce(operator.add,logicalRows)))
    print repr(columns)
    # get the maximum of each column by the string length of its items
    maxWidths = map(lambda column:max(map(lambda item,column=column:len(str(item)), column)), columns)
    rowSeparator = headerChar * (len(prefix) + len(postfix) + reduce(operator.add, maxWidths) + \
                                 len(delim)*(len(maxWidths)-1))
    # select the appropriate justify method
    justify = {'center':_center, 'right':_rjust, 'left':_ljust}[string.lower(justify)]
    output=cStringIO.StringIO()
    if sepRows: output.write(rowSeparator + '\n')
    for physicalRows in logicalRows:
        for row in physicalRows:
            output.write(prefix + 
                string.join(map(lambda (item,width),j=justify:j(str(item),width), _zip(row,maxWidths)),delim) +
                postfix + '\n')
        if (sepRows or hasHeader): 
            output.write(rowSeparator + '\n')
            hasHeader=0
    return output.getvalue()

# written by Mike Brown
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
def wrap_onspace(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line[string.rfind(line,'\n')+1:])
                         + len(string.split(word,'\n',1)[0]
                              ) >= width)],
                   word),
                  string.split(text,' ' )
                 )

import re
def wrap_onspace_strict(text, width):
    """Similar to wrap_onspace, but enforces the width constraint:
       words longer than width are split."""
    wordRegex = re.compile(r'\S{'+str(width)+r',}')
    return wrap_onspace(wordRegex.sub(lambda m: wrap_always(m.group(),width),text),width)

import math
def wrap_always(text, width):
    """A simple word-wrap function that wraps text on exactly width characters.
       It doesn't split the text in words."""
    return string.join(map( lambda i,t=text,w=width:t[w*i:w*(i+1)], range(int(math.ceil(1.*len(text)/width))) ),'\n')
    
def test():
    labels = ('First Name', 'Last Name', 'Age', 'Position')
    rows = [['John','Smith','24','Software\nEngineer'],
      ['Mary','Brohowski','23','Sales Manager'],
      ['Aristidis','Papageorgopoulos','28','Senior Reseacher']]

    print 'Without wrapping function\n'
    print renderCols([labels]+rows, hasHeader=1)
    # test indent with different wrapping functions
    width = 10
    for wrapper in (wrap_always,wrap_onspace,wrap_onspace_strict):
        print 'Wrapping function: %s(x,width=%d)\n' % (wrapper.__name__,width)
        print renderCols([labels]+rows, hasHeader=1, sepRows=1, prefix='| ', postfix=' |', wrapfunc=lambda x: wrapper(x,width))

# ks = spin.Device.get(10001).data.keys()
# l = apply(map, (None,ks) + tuple(map(lambda id:map(lambda i,id=id:str(i), spin.Device.get(id).data.values()), (10001,20001))))    
# print colrend15.renderCols(l,sepRows=1, prefix='| ', postfix=' |', justify='right', wrapfunc=lambda x:colrend15.wrap_always(x,width=40))

    # output:
    #
    #Without wrapping function
    #
    #First Name | Last Name        | Age | Position         
    #-------------------------------------------------------
    #John       | Smith            | 24  | Software Engineer
    #Mary       | Brohowski        | 23  | Sales Manager    
    #Aristidis  | Papageorgopoulos | 28  | Senior Reseacher 
    #
    #Wrapping function: wrap_always(x,width=10)
    #
    #----------------------------------------------
    #| First Name | Last Name  | Age | Position   |
    #----------------------------------------------
    #| John       | Smith      | 24  | Software E |
    #|            |            |     | ngineer    |
    #----------------------------------------------
    #| Mary       | Brohowski  | 23  | Sales Mana |
    #|            |            |     | ger        |
    #----------------------------------------------
    #| Aristidis  | Papageorgo | 28  | Senior Res |
    #|            | poulos     |     | eacher     |
    #----------------------------------------------
    #
    #Wrapping function: wrap_onspace(x,width=10)
    #
    #---------------------------------------------------
    #| First Name | Last Name        | Age | Position  |
    #---------------------------------------------------
    #| John       | Smith            | 24  | Software  |
    #|            |                  |     | Engineer  |
    #---------------------------------------------------
    #| Mary       | Brohowski        | 23  | Sales     |
    #|            |                  |     | Manager   |
    #---------------------------------------------------
    #| Aristidis  | Papageorgopoulos | 28  | Senior    |
    #|            |                  |     | Reseacher |
    #---------------------------------------------------
    #
    #Wrapping function: wrap_onspace_strict(x,width=10)
    #
    #---------------------------------------------
    #| First Name | Last Name  | Age | Position  |
    #---------------------------------------------
    #| John       | Smith      | 24  | Software  |
    #|            |            |     | Engineer  |
    #---------------------------------------------
    #| Mary       | Brohowski  | 23  | Sales     |
    #|            |            |     | Manager   |
    #---------------------------------------------
    #| Aristidis  | Papageorgo | 28  | Senior    |
    #|            | poulos     |     | Reseacher |
    #---------------------------------------------

if __name__ == '__main__':
  import sys, io
  if ( len(sys.argv) > 1 ): f = open(sys.argv[1])
  else: f = sys.stdin

  rows = []
  for l in f.readlines():
    if l[0] == '#':
      sys.stdout.write(l[1:])
    else:
      rows.append(string.split(string.strip(l),"\t"))
  cols = otranspose(rows)

  sys.stdout.write(fmtcols(cols, n_width=io.ioctl_GWINSZ(sys.stderr)[1], b_header=1))

