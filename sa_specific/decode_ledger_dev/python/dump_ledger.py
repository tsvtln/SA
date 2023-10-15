#!/opt/opsware/bin/python2

import sys, os, struct, cStringIO, string, time, traceback

SECTOR_LEN = 512

DICT_MAGIC = "\x99\x55\xee\xaa"

ENTRY_HEAD_LEN = 36

# A record is composed of key/value pairs.
# A key has form: <len> <key>
# A value has the form: <type> <len> <value>

# value datatypes:
# 01 - dictionary
# 02 - string array
#      value is of form: <num_elements> <el1_len> <el1_str> <el2_len> <el2_str> ...
#      where the lenth of each element includes the length specifier.
# 07 - binary blob
# 08 - string
# 0c - unsigned integer

TYPE_DICT = '\x01'
TYPE_STR_ARRAY = '\x02'
TYPE_TIME = '\x03'
TYPE_BIN = '\x07'
TYPE_STR = '\x08'
TYPE_BOOL = '\x09'
TYPE_DATE = '\x0b'
TYPE_UINT = '\x0c'

# value length encoding:
# 1-byte: XX             (exclusive)
# 2-byte: 79 XX XX       (inclusive)
# 4-byte: 7a XX XX XX XX (inclusive)

LEN_2_BYTE = '\x79'
LEN_4_BYTE = '\x7a'

ERR_KEY = '_errors'
def add_err(map, msg):
  if ( not map.has_key(ERR_KEY) ):
    map[ERR_KEY] = []
  map[ERR_KEY].append(msg)

def str_to_hex(str, delem=' '):
  return string.join(map(lambda c:'0123456789abcdef'[ord(c)>>4]+'0123456789abcdef'[ord(c)&0xf], str),delem)

# returns: -1 if EOF.
def read_len(stream):
  length = -1
  b1 = stream.read(1)
  if ( b1 ): 
    if ( b1 == LEN_2_BYTE ):
      b1 = stream.read(1)
      b2 = stream.read(1)
      if ( b1 and b2 ):
        length = (ord(b1) << 8) + ord(b2) - 2
    elif ( b1 == LEN_4_BYTE ):
      b1 = stream.read(1)
      b2 = stream.read(1)
      b3 = stream.read(1)
      b4 = stream.read(1)
      if ( b1 and b2 and b3 and b4 ):
        length = (ord(b1) << 24) + (ord(b2) <<168) + (ord(b3) << 8) + ord(b4) - 4
    else:
      length = ord(b1)
  return length

def remove_trailing_null(str):
  if ( (len(str) > 0) and (str[-1] == '\x00') ):
    return str[:-1]
  else:
    return str
  
# returns: '' if EOF.
def read_key(stream):
  key = ''
  # Read the key length.
  key_len = read_len(stream)
  if ( key_len > -1 ):
    key = stream.read(key_len)
    if ( len(key) < key_len ):
      key = ''
  # Remove trailing null char.
  key = remove_trailing_null(key)
  return key

def read_dict(stream):
  dict = {}
  # Extract the byte length of the dictionary
  bsize = read_len(stream)
  if ( bsize < 0 ):
    add_err(dict, 'EOF while reading dictionary byte size.')
    return dict
  dict['_byte_size'] = bsize

  # Read past the magic header.
  magic = stream.read(len(DICT_MAGIC))
  if ( len(magic) != len(DICT_MAGIC) ):
    add_err(dict, 'EOF while reading dictionary magic number.')
    return dict
  if ( magic != DICT_MAGIC ):
    add_err(dict, 'Dictionary magic number mismatch.  %s != %s' % (repr(magic), repr(DICT_MAGIC)))
    return dict

  # Read the bytes for this dictionary.
  dict_data_len = bsize - len(DICT_MAGIC)
  dict_data = stream.read(dict_data_len)
  if ( len(dict_data) < dict_data_len ):
    add_err(dict, 'EOF while reading data for dictionary.  Decoding as much as possible.')
  stream = cStringIO.StringIO(dict_data)

  while ( stream.tell() < (len(dict_data)-1) ):
    key = read_key(stream)
    if ( key ):
      dict[key] = read_val(stream)
      _decode_binary_blob(dict, key)
    else:
      add_err(dict, 'EOF while decoding dictionary key/value pairs')

  return dict

def read_str_array_el(stream):
   bsize = stream.read(1)
   if ( len(bsize) < 1 ):
     return ''
   bsize = ord(bsize) - 1
   if ( bsize < 0 ):
     return ''
   return remove_trailing_null(stream.read(bsize))

def read_str_array(stream):
#  return read_uk_type(stream, TYPE_STR_ARRAY)
  arr = []

  bsize = read_len(stream)
  if ( bsize < 0 ):
    return arr
  arr_data = stream.read(bsize)
  stream = cStringIO.StringIO(arr_data)
  arr_len = read_len(stream)
  for i in range(arr_len):
    arr.append(read_str_array_el(stream))

  return arr

def read_time(stream):
  t = read_uint(stream)
  t = t>>32+((t&0xffffffffL)/0x100000000L)
  if ( t > 0 ): return time.ctime(t)
  else: return "<epoch>"
#  return ('TYPE_TIME(%x)' % ord(TYPE_TIME), t, time.ctime(t))

def read_bin(stream):
  bsize = read_len(stream)
  return stream.read(bsize)

def read_str(stream):
  str = read_bin(stream)
  return remove_trailing_null(str)

def read_bool(stream):
  return read_uint(stream)

def read_date(stream):
  t = read_uint(stream)
  if ( t > 0 ): return time.ctime(t)
  else: return "<epoch>"
#  return ('TYPE_DATE(%x)' % ord(TYPE_DATE), t, time.ctime(t)))

def read_uint(stream):
  bsize = read_len(stream)
  uint_raw = stream.read(bsize)
  uint_raw = uint_raw + '\x00'*(bsize-len(uint_raw))
  uint = 0L
  for i in range(bsize):
    uint = uint + (ord(uint_raw[i]) << ((bsize-i-1)*8))
  return uint

def read_uk_type(stream, type):
  map = {'type':type}
  add_err(map, 'Unknown Type: 0x%x' % ord(type))
  bsize = read_len(stream)
  if ( bsize < 0 ):
    return None
  map['byte_size'] = bsize
  data = stream.read(bsize)
  if ( len(data) < bsize ):
    add_err(map, 'EOF while reading data for unknown value type.')
  map['data'] = str_to_hex(data)
  return map

g_type_reader_fns = {
  TYPE_DICT: read_dict,
  TYPE_STR_ARRAY: read_str_array,
  TYPE_TIME: read_time,
  TYPE_BIN: read_bin,
  TYPE_STR: read_str,
  TYPE_BOOL: read_bool,
  TYPE_DATE: read_date,
  TYPE_UINT: read_uint }

def read_val(stream):
  global g_type_reader_fns
  type = stream.read(1)
  if ( len(type) < 1 ):
    return None

  if ( g_type_reader_fns.has_key(type) ):
    return g_type_reader_fns[type](stream)
  else:
    return read_uk_type(stream, type)

# returns: None: EOF
def read_entry(stream):
  data = ''
  # Repeat until we find the first sector of a ledger record.
  while (1):
    # Read the next sector from the stream.
    data = stream.read(SECTOR_LEN)

    # If we didn't read in a full sector.
    if ( len(data) < SECTOR_LEN ):
      # Indicate EOF.
      return None

    # If this sector has the inner magic number
    if ( data[40:44] == DICT_MAGIC ):
      break

  entry = {}

  # Pull out the entry header.
  header = data[:ENTRY_HEAD_LEN]

  # Pull out the entry hash number
  entry['hash'] = str_to_hex(header[:8],'')

  # Pull out the payload length.
  pl_len = struct.unpack("!L", header[24:28])[0]
#  print "DEBUG: %s" % str(pl_len)
  entry['pl_len'] = pl_len

  # Calculate the number of extra sectors we need to erad to get the full entry.
  num_extra_sectors = ((ENTRY_HEAD_LEN + pl_len - 1) >> 9)

  # Read in the extra sectors for the full entry.
  extra_data_len = SECTOR_LEN * (num_extra_sectors)
  extra_data = stream.read(extra_data_len)
  data = data + extra_data
  if ( len(extra_data) < extra_data_len):
    add_err(entry, 'EOF while reading extra sectors: extra_data_len: %d, len(extra_data): %d' % (extra_data_len, len(extra_data)))

  try:
    # The container datatype is a dictionary with a 4-byte length.
    # (We need to fix up the 4-byte length to look like a "value length".)
    entry_stream = cStringIO.StringIO('\x7a' + data[ENTRY_HEAD_LEN:ENTRY_HEAD_LEN+pl_len])
    entry['contents'] = read_dict(entry_stream)
  except:
    val = entry_stream.getvalue()
    entry['contents'] = {'decode_error':string.join(apply(traceback.format_exception, sys.exc_info()),''),
                         'entry_stream':val, 'len':len(val)}

  # Return the parsed entry.
  return entry

g_dec_jo = 0

def _decode_binary_blob(dict, key):
  if ( key == 'msg' ):
    val = dict[key]
    if ( val[:4] == 'PK\x03\x04' ):
      val = _unzip(dict,val)
    if ( val[:4] == '\xac\xed\x00\x05' and g_dec_jo ):
      val = _dec_jo(dict, val)
    dict[key] = val

def _unzip(dict,val):
  zf = zipfile.ZipFile(cStringIO.StringIO(val))
  try:
    val = zf.read('o')
  except:
    dict['zip_index'] = map(lambda i:{'filename':i.filename,'compress_size':i.compress_size,'file_size':i.file_size}, zf.filelist)
  return val

def _dec_jo(dict, val):
  class_path = "/opt/opsware/vault/classes/:/opt/opsware/vault/3rdParty/opsware_common/opsware_common-latest.jar:/opt/opsware/vault/3rdParty/spin-1_0_0/spinclient-latest.jar:/opt/opsware/tibco/lib/tibrvj.jar"
  java_bin = "java"
  if ( os.environ.has_key('CLASSPATH') ):
    class_path = "%s:%s" % (os.environ['CLASSPATH'], class_path)
  if ( os.environ.has_key('JAVA_BIN') and os.environ['JAVA_BIN']):
    java_bin = os.environ['JAVA_BIN']
  cmd = "env CLASSPATH='%s' %s dec_jo -" % (class_path, java_bin)
#  print 'DEBUG: %s' % cmd
  (stdin, stdout) = os.popen2(cmd)
  stdin.write(val)
  stdin.close()
  chunk = ''
  newval = ''
  while 1:
    chunk = stdout.read(1024)
    if ( not chunk ): break
    newval = newval + chunk
  if newval: val = newval
  return val

import pprint

# If we aren't using at least python 2 then exit.
if ( int(sys.version[0]) < 2 ):
  sys.stdout.write("Requires python 2.0 or higher.\n")
  sys.exit(1)

import zipfile

# Disable the KeyboardInterrupt exception handling.
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

if ( len(sys.argv) == 1 ):
  sys.stdout.write("""Usage: dump_ledger [-j] <ledger_file1> [<ledger_file2> ...]

  -j   Attempt to recognize and deserialize java objects.  (Note, make sure
       that the $CLASSPATH environment variable contains the classes 
       neccessary to deserialize the objects.)

""")
  sys.exit(1)

if (sys.argv[1] == '-j'):
  g_dec_jo = 1
  del sys.argv[1]

for file_name in sys.argv[1:]:
  sys.stdout.write("%s:\n" % file_name)
  file = open(file_name)
  while 1:
    rec = read_entry(file)
    if ( not rec ):
      break
    try:
      pprint.pprint(rec)
    except IOError, e:
      sys.stderr.write("stdout closed.")
      sys.exit(0)
