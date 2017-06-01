from io import BytesIO
from struct import unpack, pack

class Data:
   def __init__(self,data,standard,text):
      bytes = BytesIO(data)
      self._standard = standard
      self._text = text
      self._matrix = None
      datatype = '>'
      if self._standard.BYTEORD == 'little endian':
         datatype = '<'
      o = []
      if self._standard.DATATYPE != 'F':
         raise ValueError('unsupported DATATYPE. implement in Data')
      for i in range(0,self._standard.TOT):
         f = unpack(datatype+'f'*self._standard.PAR,bytes.read(self._standard.PAR*4))
         o.append(list(f))
      self._matrix = o
   @property
   def row_count(self):
      return len(self._matrix)
   @property
   def bytes(self):
      ob = bytearray()
      datatype = '<'
      if self._standard.BYTEORD == 'big endian': datatype = '>'
      for row in self._matrix:
         v = b''.join([pack(datatype+'f',cell) for cell in row])
         ob+= v
      return bytes(ob)

   @property
   def matrix(self):
      return self._matrix
   @matrix.setter
   def matrix(self,mat):
      self._matrix = mat
      self._text['$TOT'] = len(mat) #*self._standard.PAR
