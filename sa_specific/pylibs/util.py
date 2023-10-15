import traceback,string,sys

def last_ex():
  return string.join( apply( traceback.format_exception, sys.exc_info() ), "")

def shift(l):
  r = l[0]
  del l[0]
  return r
