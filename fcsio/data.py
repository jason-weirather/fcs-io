from io import BytesIO
from struct import unpack

class Data:
   def __init__(self,data,text):
      self._bytes = BytesIO(data)
      self._text = text
      datatype = '>'
      if str(self._text['$BYTEORD']) == '1,2,3,4':
         datatype = '<'
      o = []
      for i in range(0,int(self._text['$TOT'])):
         f = unpack(datatype+'f',self._bytes.read(4))
         if i % int(self._text['$PAR'])==0: o.append([])
         o[-1].append(float(f[0]))
      self._o = o
