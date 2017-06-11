import fcsio
import re, struct
import xml.etree.ElementTree as ET
from collections import OrderedDict
from io import BytesIO

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
   @property
   def matrix(self):
      schema = self.fcsheaderschema
      mat = []
      l = len(schema.data['SegmentColumns'])
      b = BytesIO(self._raw)
      i = 0
      while b:
         i+=1
         #if i%1000000==0: print(b.tell())
         row_bytes = b.read(4*l)
         if len(row_bytes)==0: break
         vals = struct.unpack('<'+str(l)+'f',b.read(4*l))
         mat.append(list(vals))
         #print((i,b.tell(),len(self._raw)))
      return mat
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
         ostr += '# '+category
         if len(self._data[category]) > 1: ostr += " - ("+str(len(self._data[category]))+" entries)\n"
         else: ostr += "\n"
         for i,e in enumerate(self._data[category]):
           keys = e.keys()
           ostr += str(i+1)+". "+str(len(keys))+" attributes\n"
           for k in keys:
              ostr += "   "+str(k)+" \t"+str(e[k])+"\n"
      return ostr

