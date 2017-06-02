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
      self._version = None
      self._data = None
      self._text = None
      self._supplementary_text = None
      self._analysis = None
      self._other = [] # added advantage of passing by reference when doing a copy
      if bytes: self._set_from_bytes(bytes)
      if fcs: self._set_from_fcs(fcs)

   def _set_from_bytes(self,bytes):
      """ Set the FCS file according to raw data """
      header = Header(bytes)
      self._version = header.version
      self._other = [bytes[x.start:x.end+1] for x in header.other_ranges]
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
      data_segments = [self.standard.ENDDATA,self.standard.ENDANALYSIS,
                       self.standard.ENDSTEXT,header.text_range.end]
      for o in header.other_ranges: data_segments.append(o.end)
      start =  self.standard.BEGINSTEXT
      end = self.standard.ENDSTEXT
      if start > 0 and end > 0:
         self._supplementary_text = Text(bytes[start:end+1])
      if self._supplementary_text:
         raise ValueError('Supplementary text is present but still needs to be impelemented')

      """This CRC doesn't seem all that useful but we could probably
         use it as a more strict validation check"""
      if self.standard.NEXTDATA == 0:
         """we can only do a CRC if this is the only dataset"""
         lastend = sorted(data_segments)[-1]
         crc_bytes = bytes[lastend+1:lastend+9]

      """header will need to be reconstructed"""
   def _set_from_fcs(self,fcs):
      self._version = fcs.version
      self._text = Text(fcs.text.bytes)
      self._data = Data(fcs.data.bytes,self.standard,self._text)
      """ Set the FCS file according to another FCS file

      We may want to ignore analysis and other later
      """
      self._other = fcs._other
      self._analysis = fcs._analysis
      self._supplementary_text = fcs._supplementary_text

   def copy(self):
      """Output an fcs object that is the same content as self

      Creates a new object for everything EXCEPT the OTHER fields
      (for now)

      """
      return FCS(fcs=self)
   @property
   def version(self):
      return self._version
   def construct_fcs(self,essential=False): return _ConstructedFCS(self,essential)
   """constructed_fcs makes the header"""
   @property
   def text(self):
      return self._text
   @property
   def data(self):
      return self._data
   @property
   def other(self):
      """returns a list of others"""
      return self._other
   @property
   def other_segments(self): return self._other_segments
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

class _ConstructedFCS:
   """A class to hold a created header and byte values
   so that data and text bytes corresponding to the header
   don't need to be recomputed"""
   def __init__(self,fcs,essential=False):
      self._essential=essential # only output the essential data?
      self._other = fcs._other #set this early on because we may want to skip it
      if self._essential: self._other = []
      """header is reconstructed"""
      basic_header_length = 58
      other_padding_length = 20

      hsize = basic_header_length + other_padding_length*2*len(self._other)
      """adjust hsize if we are sticking only to the essential"""

      old_text_bytes = fcs.text.bytes
      text_start = hsize
      text_end = text_start + len(old_text_bytes) - 1

      """ There is a bit of a conundrum.
          We need to set the TEXT size, but part of the TEXT
          is the data_start and data_end. Setting data_start and data_end
          could change the size of TEXT, thus changing data_start and
          data_end.  Thanks for that. """

      text_buffer = 100 # add a buffer to fix this

      data_bytes = fcs.data.bytes
      real_data_start = text_end + text_buffer + 1
      real_data_end = real_data_start + len(data_bytes)-1
      data_start = real_data_start # for display
      data_end = real_data_end
      fcs.standard.BEGINDATA = data_start
      fcs.standard.ENDDATA = data_end

      text_bytes = fcs.text.bytes
      dif = text_buffer-(len(text_bytes)-len(old_text_bytes))
      if len(text_bytes) - len(old_text_bytes) > 100: raise ValueError('problem in conundrum condition in header constructor. buffer is not working right. implementation problem')
      text_end = text_start+len(text_bytes)-1

      if data_end > 99999999:
         """so ugly. but this is the case for large data. you get it from TEXT"""
         data_start = 0
         data_end = 0

      """need to implement analysis some day"""
      analysis_start = 0
      analysis_end = 0

      """ Put other segements after the supplemental text """
      if fcs.standard.BEGINSTEXT != 0:
          raise ValueError('Need to implement supplemental text here')
      """set the positions for the OTHER segments"""
      other_prev = sorted([real_data_end,
                           analysis_end,
                           fcs.standard.ENDSTEXT])[-1]
      other_str = ''
      for segment in self._other:
         other_str += str(other_prev+1).rjust(other_padding_length)
         other_str += str(other_prev+len(segment)).rjust(other_padding_length)
         other_prev += len(segment)
      ostr =  fcs.version.ljust(10)
      ostr += str(text_start).rjust(8) # TEXT start
      ostr += str(text_end).rjust(8) # TEXT end
      ostr += str(data_start).rjust(8)
      ostr += str(data_end).rjust(8)
      ostr += str(analysis_start).rjust(8)
      ostr += str(analysis_end).rjust(8)
      ostr += other_str
      """accessable properties"""
      self.header_bytes = bytes(ostr,'ascii')
      self.text_bytes = text_bytes
      self._dif = dif
      self.data_bytes = data_bytes
   @property
   def fcs_bytes(self):
      return self.header_bytes+\
             self.text_bytes+\
             bytes(' '*self._dif,'ascii')+\
             self.data_bytes+\
             b''.join(self._other)+\
             bytes('0'*8,'ascii') # add the CRC
   def __str__(self):
      """Just print the header with spaces replaced with astrix characters"""
      return self.header_bytes.decode('ascii').replace(' ','*')
