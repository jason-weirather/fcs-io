import struct, re
from io import BytesIO
from fcsio.header import Header
from fcsio.text import Text
from fcsio.data import Data
from fcsio.text.parameters import Parameters
from fcsio.text.standard import Standard
from fcsio.filter import Filter

class FCS:
   def __init__(self,bytes=None,fcs=None):
      self._user_defined_segment = None
      self._data = None
      if bytes:
         """ Set the FCS file according to raw data """
         header = Header(bytes)
         if header.user_defined_segment_range.in_header:
            self._user_defined_segment = bytes[header.user_defined_segment_range.start:
                                               header.user_defined_segment_range.end+1]
         self._text = Text(bytes[header.text_range.start:
                                 header.text_range.end+1])
         if header.data_range.in_header:
            """We can read data from the header range"""
            self._data = Data(bytes[header.data_range.start:
                                    header.data_range.end+1],
                              self.standard,self._text)
         else:
            """We couldn't read data range from the header try the text"""
            self._data = Data(bytes[self.standard.BEGINDATA:
                                    self.standard.ENDDATA+1],
                              self.standard,self._text)

      """header will need to be reconstructed"""
      if fcs:
         """ Set the FCS file according to another FCS file """
         """ We may want to ignore the user defined segment for speed reasons"""
         if self._user_defined_segment:
            self._user_defined_segment = fcs.user_defined_segment[:]
         self._text = Text(fcs.text.bytes)
         self._data = Data(fcs.data.bytes,self.standard,self._text)

      self._analysis = None
      self._other = None
      self._supplementary_text = None

      start =  self.standard.BEGINSTEXT
      end = self.standard.ENDSTEXT
      if start > 0 and end > 0:
         self._supplementary_text = Text(bytes[start:end+1])
      if self._supplementary_text:
         raise ValueError('Supplementary text is present but still needs to be impelemented')
   def copy(self):
      """Output an fcs object that is the same content as self"""
      return FCS(fcs=self)
   @property
   def header(self):
      return self._header
   @property
   def text(self):
      return self._text
   @property
   def data(self):
      return self._data
   @property
   def user_defined_segment(self): return self._user_defined_segment
   @property
   def parameters(self):
      """Parameters needs to be accessed after both text and data have
      been intialized because data is coupled to parameters. Any changes
      is parameters will also affect data."""
      return Parameters(self.text,self.data)
   @property
   def standard(self):
      """access and set where possible standard TEXT fields through here"""
      return Standard(self._text)
   @property
   def filter(self):
      return Filter(self)
