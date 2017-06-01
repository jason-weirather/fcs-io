import struct, re
from io import BytesIO
from fcsio.header import Header
from fcsio.text import Text
from fcsio.data import Data


_param = {'B':'Number of bits reserved for parameters n',
          'E':'Amplification type for parameter n',
          'N':'Short name for parameter n',
          'R':'Range for parameter number n',
          'CALIBRATION':'Conversion of parameter values to any well defined units, e.g. MESF',
          'D':'Suggested visualization scale for parameter n',
          'F':'Name of optical filter for parameter n',
          'G':'Amplifier gain used for aquisition of parameter n',
          'L':'Excitation wavelength(s) for parameter n',
          'O':'Excitation power for parameter n',
          'P':'Percent of emitted light collected by parameter n',
          'S':'Name used for parameter n',
          'T':'Detector type for parameter n',
          'V':'Detector voltage for parameter n'}

class FCS:
   def __init__(self,bytes):
      header = Header(bytes) #[0:58])
      """header will need to be reconstructed"""
      self._user_defined_segment = None
      if header.user_defined_segment_range.in_header:
         self._user_defined_segment = bytes[header.user_defined_segment_range.start:
                                            header.user_defined_segment_range.end+1]
      self._text = Text(bytes[header.text_range.start:
                              header.text_range.end+1])
      print(self._text)
      self._data = None
      if header.data_range.in_header:
         """We can read data from the header range"""
         self._data = Data(bytes[header.data_range.start:
                                 header.data_range.end+1],
                           self._text)
      else:
         """We couldn't read data range from the header try the text"""
         self._data = Data(bytes[self._text.standard.BEGINDATA:
                                 self._text.standard.ENDDATA+1],
                           self._text)
      self._analysis = None
      self._other = None
      self._supplementary_text = None
      start =  int(self.text['$BEGINSTEXT'])
      end = int(self.text['$ENDSTEXT'])
      if start > 0 and end > 0:
         self._supplementary_text = Text(bytes[start:end+1])
      if self._supplementary_text:
         raise ValueError('Supplementary text is present but still needs to be impelemented')
   @property
   def header(self):
      return self._header
   @property
   def text(self):
      return self._text
   @property
   def data(self):
      return
      if self._data: return self._data
      """ If we have data lets get the object """
      start = self.header.data_range.start
      end = self.header.data_range.end
      if start != 0 and end != 0:
         self._data = Data(self._bytes[start:end+1],
                           self.text,
                      )
         return self._data
      """ If we are still here """
      start = int(self.text['$BEGINDATA'])
      end = int(self.text['$ENDDATA'])
      if start != 0 and end != 0:
         self._data = Data(self._bytes[start:end+1],
                           self.text,
                      )
         return self._data
      sys.stderr.write("Warning no error\n")
      return None
