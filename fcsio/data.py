from io import BytesIO
from struct import unpack, pack

class Data:
   """The class for working with the data attached to an fcs object

   :param data: bytes of the Data segment
   :param standard: class for interfacing with the TEXT
   :param text: main TEXT class
   :type data: bytearray
   :type standard: :class:`fcsio.text.standard.Standard`
   :type text: :class:`fcsio.text.Text`
   """
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
   def event_count(self):
      """Get the number of events

      :return: the event count
      :rtype: int
      """
      return len(self.matrix)
   @property
   def bytes(self):
      """Get the data

      :return: constructed data
      :rtype: bytearray
      """
      ob = bytearray()
      datatype = '<'
      if self._standard.BYTEORD == 'big endian': datatype = '>'
      for row in self._matrix:
         v = b''.join([pack(datatype+'f',cell) for cell in row])
         ob+= v
      return bytes(ob)

   @property
   def matrix(self):
      """Get the data matrix

      :return: stored data matrix
      :rtype: 2D matrix list of rows, rows are lists of float
      """
      return self._matrix
   @matrix.setter
   def matrix(self,mat):
      self._matrix = mat
      self._text['$TOT'] = len(mat) #*self._standard.PAR
