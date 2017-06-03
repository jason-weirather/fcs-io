
import struct, re
from io import BytesIO
from fcsio.header import Header
from fcsio.text import Text
from fcsio.data import Data
from fcsio.text.parameters import Parameters
from fcsio.text.standard import Standard
from fcsio.filter import Filter

class FCS:
   """The primary class for working with FCS file data is the FCS class.

   :param bytes: The raw data of the FCS file
   :param fcs: :class:`fcsio.FCS` object to create a new FCS from. Used by copy.
   :type bytes: bytearray
   :type fcs: fcsio.FCS

    You must specify either bytes or fcs.  not both.
    """
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

      .. warning:: The copy is not a perfect copy. OTHER fields are still
                   passsed by reference. And no attempt is made at outputing
                   identical bytes as input.  If you need a completely new
                   FCS object unlinked to the old, you can use
                   `totally_new = FCS(myoldfcs.construct_fcs().fcs_bytes)`

      :return: Make a new FCS object htat is a copy of this one.
      :rtype: :class:`fcsio.FCS`
      """
      return FCS(fcs=self)

   def construct_fcs(self,essential=False):
      """To get an actual file out of an FCS object the
      construct_fcs method is required to be called.

      :param essential: An optional argument, where if set to True, will trim off the OTHER segements. The other objects are passed as references so clearing them may not be generally necessary for conserving memory.
      :type essential: bool
      :return: Generate an object with methods necessary for outputing a new FCS file (bytes that can be written)
      :rtype: :class:`fcsio.StagedFCS`
      """
      return StagedFCS(self,essential)
   @property
   def version(self):
      """Version as listed in the first 10 bytes of the header

      :return: version
      :rtype: string
      """
      return self._version
   @property
   def text(self):
      """access the TEXT segment

      .. note:: The object containing the TEXT segment initially
                separates the keywords from per-parameter keywords. The
                per-parameter information is better accessed through the
                FCS property :class:`fcsio.FCS.parameters` . The standard FCS
                keywords are accessible via properties of the :class:`fcsio.FCS.standard` .
                This is a better choice for getting and setting values if you want to
                use more logical types instead of strings for everything.  Finally
                keep in mind that although TEXT may contain information such as
                DATABEGINS or DATAENDS, these values are not updated until the
                :class:`fcsio.FCS.construct_fcs` method is called.  At this point they
                will be updated.

      :alsosee: :class:`fcsio.FCS.parameters`
      :alsosee: :class:`fcsio.FCS.standard`

      :return: Get the object for accessing the TEXT segment data
      :rtype: :class:`fcsio.text.Text`
      """
      return self._text

   @property
   def data(self):
      """access the DATA segment

      :return: Get an object for accessing the DATA segment
      :rtype: :class:`fcsio.data.Data`
      """
      return self._data
   @property
   def other(self):
      """access the OTHER segments (user defined fields specified at the end of the header)

      :return: Get the data from OTHER user defined segments at the end of the header
      :rtype: list of bytearrays
      """
      return self._other
   @property
   def parameters(self):
      """Parameters needs to be accessed after both text and data have
      been intialized because data is coupled to parameters. Any changes
      is parameters will also affect data.

      :return: get an object for accessing/modifying paramters
      :rtype: :class:`fcsio.text.parameters.Parameters`
      """
      return Parameters(self.text,self.data)
   @property
   def standard(self):
      """access and set where possible standard TEXT fields through here.
      You can access these fields through :class:`fcsio.text.Text` also but
      are limited to string input and outputs.

      :alsosee: :class:`fcsio.text.Text`
      :return: get an object for accessing/modifying standard keywords in TEXT
      :rtype: :class:`fcsio.text.standard.Standard`
      """
      return Standard(self._text)
   @property
   def filter(self):
      return Filter(self)

class StagedFCS:
   """A class to hold a created header and byte values
   so that data and text bytes corresponding to the header
   don't need to be recomputed

   :param fcs: The FCS object being staged for output
   :param essential: if True, trim off the OTHER segements
   :type fcs: :class:`fcsio.FCS`
   :type essential: bool
   """
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
