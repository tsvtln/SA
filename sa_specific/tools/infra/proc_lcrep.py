

class Fld:
  def __init__(self, s_name, n_off, n_len):
    pass

class StrFld(Fld):
  def __init__(*args, **kwargs):
    Fld.__init__(*args, **kwargs)

class NumFld(Fld):
  def __init__(*args, **kwargs):
    Fld.__init__(*args, **kwargs)

class DateFld(NumFld):
  def __init__(*args, **kwargs):
    Fld.__init__(*args, **kwargs)

class Table:
  def __init__(self, s_name, lst_flds):
    self.s_name = s_name
    self.lst_flds = lst_flds

  def itterator(self):
    pass

class Index:
  def __init__(self, lst_flds, n_pos):
    pass

class Database:
  def __init__(self, s_filename=None, mode="r", fileobj=None):
    if ( fileobj is not None ):
      self.fo = fileobj
    else:
      self.fo = open(s_filename, mode)

    if ( mode == "w" ):
      self.fo.write("\0")
      self.map_tabs = {}
    elif ( mode == "r" ):
      selt.map_tabs = self._load_tables()

  def add_table(self, tab):
    self.map_tabs[tab.s_name] = tab
