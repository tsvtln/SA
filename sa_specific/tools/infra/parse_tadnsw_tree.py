import sys,struct,time

# Based on "/soft/ionian/discover/SOURCE/tadnsw/tCSWTreeFile.cpp"

#//////////////////////////////////
#// File Format:
#//
#// BYTE:  RecordID
#//   0 = Drive
#//   1 = Footprint
#//   2 = Directory
#//   3 = End of Footprint List
#//   4 = End of Directory
#//   5 = End of Drive
#//  -1 = End of File
#//-------------------------------
#// If RecordID = 1 or 2:
#//
#// BYTE   TextLen
#// CHAR   RecordText
#//-------------------------------
#// If RecordID = 1
#//
#// Windows:
#// LONG   FileSize
#// LONG   FileDateLow
#// LONG   FileDateHigh
#//
#// Unix:
#// off_t  FileSize
#// time_t FileDate
#//
#//////////////////////////////////

DRIVE = 0
FOOTPRINT = 1
DIRECTORY = 2
FOOTPRINT_END = 3
DIRECTORY_END = 4
DRIVE_END = 5
END_OF_TREE = -1

map_rec_ids = { DRIVE:         "Drive",
                FOOTPRINT:     "Footprint",
                DIRECTORY:     "Directory",
                FOOTPRINT_END: "End of Footprint List",
                DIRECTORY_END: "End of Directory",
                DRIVE_END:     "End of Drive",
                END_OF_TREE:   "End of File" }

def shift(l):
  r = l[0]
  del l[0]
  return r

def msg(s, args=None):
  if ( args is not None ):
    s = s % args
  sys.stdout.write(s)
  sys.stdout.flush()

fn = None
endian = ""
args = sys.argv[1:]
while (len(args) > 0):
  cur_arg = shift(args)
  if ( cur_arg == "-le" ):
    endian = "<"
  elif ( cur_arg == "-be" ):
    endian = ">"
  else:
    fn = cur_arg

if ( fn is None ):
  msg("Usage: %s <AISW.TRE> [-le|-be]\n" % sys.argv[0])
  sys.exit(1)

f = open(fn)

# skip checksum
f.seek(2)

s_indent = ""
s_indent_delta = "  "
while 1:
  try:
    rec_id = ord(f.read(1))
    if ( rec_id in (FOOTPRINT, DIRECTORY) ):
      name_len = ord(f.read(1))
      name = f.read(name_len)
    if ( rec_id == FOOTPRINT ):
      (file_len,file_dt) = struct.unpack("%sII" % endian,f.read(8))
      msg("%s/%s (len=%d, %r)\n", (s_indent, name,file_len,time.ctime(file_dt)))
    elif ( rec_id == DIRECTORY ):
      msg("%s/%s\n", (s_indent,name))
      s_indent = s_indent + s_indent_delta
    elif ( rec_id == DIRECTORY_END ):
      s_indent = s_indent[len(s_indent_delta):]
    elif ( rec_id == DRIVE_END ):
      break
  except IOError, e:
    break
  except KeyboardInterrupt, e:
    break

