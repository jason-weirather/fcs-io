import fcsio
import re
import xml.etree.ElementTree as ET
from collections import OrderedDict

class FCS(fcsio.FCS):
   """Extend the FCS class for CyTOF specific features"""
   def __init__(self, *args,**kwargs):
      self._cytof = None # cache processing the OTHER field
      super().__init__(*args,**kwargs)
   @property
   def cytof(self):
      if self._cytof: return self._cytof
      # get the cytof specific dat
      if len(self.other) <= 0:
         raise ValueError('Not a compatible CyTOF FCS because no OTHER data')
      self._cytof = CyTOFOther(self.other[0])
      return self._cytof
class CyTOFOther:
   def __init__(self,bytes):
      m = re.match('<([^>]+)>',bytes.decode('utf-8','ignore'))
      if not m: raise ValueError('Not a compatible FCS because not xml in OTHER')
      tag1 = re.match('(\S+)',m.group(1)).group(1)
      m = re.search('</'+tag1+'>',bytes.decode('utf-8','ignore'))
      if not m: raise ValueError('Unterminated xml')
      self._xml = bytes[0:m.span()[1]].decode('utf-8')
      self._raw = bytes[m.span()[1]:]

   @property
   def xml(self): return self._xml
   @property
   def fcsheaderschema(self):
      return FCSHeaderSchema(self._xml)

class FCSHeaderSchema:
   """This is the xml that contains a lot of nice meta data"""
   def __init__(self,xml):
      root = ET.fromstring(xml)
      self._data = OrderedDict()
      for child in root:
         category = re.search('([^}]+$)',child.tag).group(1)
         if category not in self._data: self._data[category] = []
         self._data[category].append(OrderedDict())
         for grandchild in child:
            attribute = re.search('([^}]+$)',grandchild.tag).group(1)
            text = grandchild.text
            self._data[category][-1][attribute] = text
   @property
   def data(self): return self._data
   def __str__(self):
      ostr = ''
      for category in self._data:
         ostr += '# '+category+"\n"
      return ostr
