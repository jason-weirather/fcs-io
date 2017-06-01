from io import BytesIO
from struct import unpack

class Data:
   def __init__(self,data,text):
      print(len(data))
      self._bytes = BytesIO(data)
      self._text = text
      datatype = '>'
      if self._text.standard.BYTEORD == 'little endian':
         datatype = '<'
      o = []
      for i in range(0,self._text.standard.TOT):
         f = unpack(datatype+'f',self._bytes.read(4))
         if i % int(self._text.standard.PAR)==0: o.append([])
         o[-1].append(float(f[0]))
      self._o = o
