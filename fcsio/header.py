import re
from io import BytesIO
from collections import namedtuple

ByteIndecies = namedtuple('ByteIndecies',['start','end','in_header'])
"""One indexed byte locations of start and end"""

class Header:
   def __init__(self,data):
      self._data = data
      self._stream = BytesIO(self._data)
      """3.0 from the spec 1997 Seamer Current Protocols in Cytometry

         1. FCS 3.0 followed by spaces 00-09
         2. ASCII-encoded offset to first byte of TEXT segment 10–17
         3. ASCII-encoded offset to last byte of TEXT segment 18–25
         4. ASCII-encoded offset to first byte of DATA segment 26–33
         5. ASCII-encoded offset to last byte of DATA segment 34–41
         6. ASCII-encoded offset to first byte of ANALYSIS segment 42–49
         7. ASCII-encoded offset to last byte of ANALYSIS segment 50-57

         ByteIndecies tell the 'start', the 'end' and whether or not
         (bool) a numerical range was read from the header. If no
         numerical range was reported it is likely either absent from
         the file or coded in the TEXT

         :param text_range: namedtuple start and end bytes of TEXT
         :param data_range: namedtuple start and end bytes of DATA
         :param analysis_range: namedtuple start and end bytes of ANALYSIS
         :type text_range: ByteIndecies
         :type data_range: ByteIndecies
         :type analysis_range: ByteIndecies
         """
      b = BytesIO(self._data[0:58])
      h1 = b.read(10).decode('ascii') # 0-9
      h2 = b.read(8).decode('ascii') # 10-17
      h3 = b.read(8).decode('ascii') # 18-25
      h4 = b.read(8).decode('ascii') # 26-33
      h5 = b.read(8).decode('ascii') # 34-41
      h6 = b.read(8).decode('ascii') # 42-49
      h7 = b.read(8).decode('ascii') # 50-57
      self._s = [h1,h2,h3,h4,h5,h6,h7]
      if not self.validate():
         sys.stderr.write("Warning: header did not validate\n")
   @property
   def version(self):
      """Process the version string to remove the padding"""
      return self._s[0].rstrip()
   @property
   def text_range(self):
      """Should be between the end of the header and less than 99,999,999"""
      (start,end) = (int(self._s[1]),int(self._s[2]))
      return ByteIndecies(start,end,
             start!=0 and end!=0)
   @property
   def data_range(self):
      (start,end) = (int(self._s[3]),int(self._s[4]))
      return ByteIndecies(start,end,
             start!=0 and end!=0)
   @property
   def analysis_range(self):
      (start,end) = (int(self._s[5]),int(self._s[6]))
      return ByteIndecies(start,end,
             start!=0 and end!=0)
   def validate(self):
      """Validate for 3.0 and 3.1 together for now"""
      if not self._s[0][0:6] == 'FCS3.0' and not self._s[0][0:6] == 'FCS3.1':
         return False
      """make sure the ranges make sense"""
      for i in range(2,7):
         if not re.match('[ ]*\d+$',self._s[i]): return False
      """3.0 and 3.1 have the same header end and thus text start"""
      if self.text_range.start != 58: return False
      if self.text_range.end < 58: return False
      if self.text_range.end > 99999999: return False
      return True
   def __str__(self):
      """return the actual header"""
      return ''.join(self._s)
