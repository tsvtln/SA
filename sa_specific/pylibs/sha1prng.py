#   This module is intended to supply a python based implementation of Sun
# Java's SHA1PRNG from "sun/security/provider/SecureRandom.java".
#

import sha,string,types

def _j_byte_to_int(i):
  return (i & 0x7f) - (i & 0x80)

class sha1prng:
  def __init__(self, seed):
    self.state = None
    self.remainder = None
    self.remCount = 0
    self.digest = sha.sha()
    self.setSeed(seed)

  def _update(self, val):
    return self.digest.update(string.join(map(chr, val), ""))

  def _digest(self, val=None):
    if ( val is not None ):
      self._update(val)
    res = self.digest.digest()
    self.digest = sha.sha()
    return map(ord, res)

  def setSeed(self, seed):
    if ( self.state is not None ):
      self._update(seed)
      self.state = map(lambda i:0, self.state)
    self.state = self._digest(seed)

  def update_state(self, state, output):
    last = 1 #int
    v = 0    #int
    t = 0    #byte
    zf = 0   #boolean

    i = 0    #int
    while ( i < len(state) ):
      v = _j_byte_to_int(state[i]) + _j_byte_to_int(output[i]) + last
      t = v & 0xff
      zf = zf | (state[i] != t)
      state[i] = t
      last = v >> 8
      i = i + 1

    if (not zf):
      state[0] = (state[0] + 1) & 0xff

  # Modifies: <result>
  def next_bytes(self, result):
    index = 0  #int
    todo = 0   #int
    output = self.remainder  #list of bytes

    if ( self.state is None ):
      # for now lets throw an error, but later we could also auto intialize 
      # seed from something random. -dw
      raise Exception("Not yet seeded.")

    r = self.remCount  # int
    if ( r > 0 ):
      todo = ((len(result) - index) < (self.digest.digestsize - r)) and (len(result) - index) or (self.digest.digestsize - r)
      i = 0
      while ( i < todo ):
        result[i] = output[r]
        output[r] = 0
        r = r + 1
        i = i + 1
      self.remCount = self.remCount + todo
      index = index + todo

    while ( index < len(result) ):
      self._update(self.state)
      output = self._digest()
      self.update_state(self.state, output)

      todo = ((len(result) - index) > self.digest.digestsize) and self.digest.digestsize or (len(result) - index)
      i = 0
      while ( i < todo ):
        result[index] = output[i]
        index = index + 1
        output[i] = 0
        i = i + 1
      self.remCount = self.remCount + todo

    self.remainder = output
    self.remCount = self.remCount % self.digest.digestsize
