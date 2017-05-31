from io import BytesIO
from struct import unpack

class Data:
   def __init__(self,data,text):
      self._bytes = BytesIO(data)
      self._text = text
      print(self._text['$TOT'])
      print(self._text['$MODE'])
      print(str(self._text['$DATATYPE']))
      datatype = '>' #big endian
      if str(self._text['$DATATYPE']) == '1,2,3,4':
         sys.stderr.write("hi\n")
         datatype = '<'
      print(self._text['$BYTEORD'])
      print(self._text['$P1R'])
      print(self._text['$P1B'])
      for i in range(0,int(self._text['$TOT'])):
         f = unpack(datatype+'f',self._bytes.read(4))
         #print(f)
      print(len(data))
      return
