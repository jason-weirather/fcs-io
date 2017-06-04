import re, sys
from io import BytesIO
from collections import namedtuple

ByteIndecies = namedtuple('ByteIndecies',['start','end','in_header'])
"""1-indexed byte locations of start and end with a bool specifying if it was defined in the header or not"""

class Header:
   """The header class is only used temporarily when reading the FCS from
   data.  The version is the only value that doesn't change depending on
   how the data is altered.

   3.0 from the spec 1997 Seamer Current Protocols in Cytometry

   1. FCS 3.0 followed by spaces 00-09
   2. ASCII-encoded offset to first byte of TEXT segment 10–17
   3. ASCII-encoded offset to last byte of TEXT segment 18–25
   4. ASCII-encoded offset to first byte of DATA segment 26–33
   5. ASCII-encoded offset to last byte of DATA segment 34–41
   6. ASCII-encoded offset to first byte of ANALYSIS segment 42–49
   7. ASCII-encoded offset to last byte of ANALYSIS segment 50-57
   8. OTHER segments 58 to start of TEXT

   :class:`fcsio.header.ByteIndecies` tell the 'start', the 'end' and whether or not
   (bool) a numerical range was read from the header. If no
   numerical range was reported it is likely either absent from
   the file or coded in the TEXT

   :param data: The FCS file data (not just the first 58 bytes)
   :type data: bytearray
   """
   def __init__(self,data):
      self._data = data
      self._stream = BytesIO(self._data)
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
      """ get the version

      :return: version string from the beginning of the header with whitespace removed
      :rtype: string
      """
      return self._s[0].rstrip()
   @property
   def text_range(self):
      """Should be between the end of the header and less than 99,999,999

      :return: get the text range. it is required to be present.
      :rtype: :class:`fcsio.header.ByteIndecies`
      """
      (start,end) = (int(self._s[1]),int(self._s[2]))
      return ByteIndecies(start,end,
             start!=0 and end!=0)
   @property
   def data_range(self):
      """Can be zero if the end exceeds 99,999,999. To indicate
      it is set within the TEXT segment.

      :return: get the data range. it is required to be present.
      :rtype: :class:`fcsio.header.ByteIndecies`
      """
      (start,end) = (int(self._s[3]),int(self._s[4]))
      return ByteIndecies(start,end,
             start!=0 and end!=0)
   @property
   def analysis_range(self):
      """Can be zero if the end exceeds 99,999,999. To indicate
      it is set within the TEXT segment. or that its absent.

      :return: get the analysis range. it is required to be present.
      :rtype: :class:`fcsio.header.ByteIndecies`
      """
      (start,end) = (int(self._s[5]),int(self._s[6]))
      return ByteIndecies(start,end,
             start!=0 and end!=0)
   def validate(self,verbose=True):
      """Validate for 3.0 and 3.1 together for now

      :return: Is it a valid header?
      :rtype:  bool
      """
      if not self._s[0][0:6] == 'FCS3.0' and not self._s[0][0:6] == 'FCS3.1':
         if verbose: sys.stderr.write("Validation failure FCS version: "+self._s[0][0:6]+"\n")
         return False
      #make sure the ranges make sense
      for i in range(2,7):
         if not re.match('[ ]*\d+$',self._s[i]):
            if verbose: sys.stderr.write("Validation failure range nonsense: "+self._s[i]+"\n")
            return False
      #3.0 and 3.1 have the same header end and thus text start
      if self.text_range.start < 58: return False
      if self.text_range.end < 58: return False
      if self.text_range.end > 99999999: return False
      return True
   @property
   def other_ranges(self):
      """If there is extra data in the header return it

      Assume pairs of coordinates for now as the only thing we'll see
      for one or more user segments.

      :return: Get the coordinates of OTHER segements
      :rtype: list of :class:`fcsio.header.ByteIndecies`
      """
      if self.text_range.start == 58: return []
      dat = self._data[58:self.text_range.start].decode('ascii')
      r = tuple(re.split('\s+',dat.strip()))
      if len(r) < 2: raise ValueError('Error expected at least two OTHER values in OTHER: '+dat)
      if len(r) % 2 != 0:
         raise ValueError('Error: User defined segement doesnt have pairs of values: '+dat)
      prog = re.compile('^\d+$')
      if (not prog.match(r[0])) or (not prog.match(r[1])):
         raise ValueError('Error: User defined segement has non numeric range: '+dat)
      rp = zip(r[0::2],r[1::2])
      return [ByteIndecies(int(x[0]),int(x[1]),
                          int(x[0]) != 0 and int(x[1]) != 0) for x in rp]
   def __str__(self):
      """return the actual header"""
      return ''.join(self._s)
