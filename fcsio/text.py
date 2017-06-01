import re, sys, json
from io import BytesIO
from collections import namedtuple
from fcsio.parameter import Parameter

_required_keywords = {
   '$BEGINANALYSIS':'Byte-offset to the beginning of the ANALYSIS segment.',
   '$BEGINDATA':'Byte-offset to the beginning of the DATA segment.',
   '$BEGINSTEXT':'Byte-offset to the beginning of a supplemental TEXT segment.',
   '$BYTEORD':'Byte order for data acquisition computer.',
   '$DATATYPE':'Type of data in DATA segment (ASCII, integer, floating point).',
   '$ENDANALYSIS':'Byte-offset to the last byte of the ANALYSIS segment.',
   '$ENDDATA':'Byte-offset to the last byte of the DATA segment.',
   '$ENDSTEXT':'Byte-offset to the last byte of a supplemental TEXT segment.',
   '$MODE':'Data mode (list mode - preferred, histogram - deprecated).',
   '$NEXTDATA':'Byte offset to next data set in the file.',
   '$PAR':'Number of parameters in an event.',
   '$PnB':'Number of bits reserved for parameter number n.',
   '$PnE':'Amplification type for parameter n.',
   '$PnN':'Short name for parameter n.',
   '$PnR':'Range for parameter number n.',
   '$TOT':'Total number of events in the data set.',
   }

_optional_keywords = {
   '$ABRT' :'Events lost due to data acquisition electronic coincidence.',
   '$BTIM' :'Clock time at beginning of data acquisition.',
   '$CELLS' :'Description of objects measured.',
   '$COM' :'Comment.',
   '$CSMODE' :'Cell subset mode, number of subsets to which an object may belong.',
   '$CSVBITS' :'Number of bits used to encode a cell subset identifier.',
   '$CSVnFLAG' :'The bit set as a flag for subset n.',
   '$CYT' :'Type of flow cytometer.',
   '$CYTSN':' Flow cytometer serial number.',
   '$DATE' :'Date of data set acquisition.',
   '$ETIM' :'Clock time at end of data acquisition.',
   '$EXP' :'Name of investigator initiating the experiment.',
   '$FIL' :'Name of the data file containing the data set.',
   '$GATE' :'Number of gating parameters.',
   '$GATING' :'Specifies region combinations used for gating.',
   '$GnE' :'Amplification type for gating parameter number n (deprecated).',
   '$GnF': 'Optical filter used for gating parameter number n (deprecated).',
   '$GnN': 'Name of gating parameter number n (deprecated).',
   '$GnP': 'Percent of emitted light collected by gating parameter n (deprecated).',
   '$GnR': 'Range of gating parameter n (deprecated).',
   '$GnS': 'Name used for gating parameter n (deprecated).',
   '$GnT': 'Detector type for gating parameter n (deprecated).',
   '$GnV': 'Detector voltage for gating parameter n (deprecated).',
   '$INST': 'Institution at which data was acquired.',
   '$LAST_MODIFIED': 'Timestamp of the last modification of the data set.',
   '$LAST_MODIFIER': 'Name of the person performing last modification of a data set.',
   '$LOST': 'Number of events lost due to computer busy.',
   '$OP': 'Name of flow cytometry operator.',
   '$ORIGINALITY': 'Information whether the FCS data set has been modified (any part of it) or is original as acquired by the instrument.',
   '$PKn': 'Peak channel number of univariate histogram for parameter n (deprecated).',
   '$PKNn': 'Count in peak channel of univariate histogram for parameter n (deprecated).',
   '$PLATEID': 'Plate identifier.',
   '$PLATENAME': 'Plate name.',
   '$PnCALIBRATION': 'Conversion of parameter values to any well defined units, e.g., MESF.',
   '$PnD': 'Suggested visualization scale for parameter n.',
   '$PnF': 'Name of optical filter for parameter n.',
   '$PnG': 'Amplifier gain used for acquisition of parameter n.',
   '$PnL': 'Excitation wavelength(s) for parameter n.',
   '$PnO': 'Excitation power for parameter n.',
   '$PnP': 'Percent of emitted light collected by parameter n.',
   '$PnS': 'Name used for parameter n.',
   '$PnT': 'Detector type for parameter n.',
   '$PnV': 'Detector voltage for parameter n.',
   '$PROJ': 'Name of the experiment project.,',
   '$RnI': 'Gating region for parameter number n.',
   '$RnW': 'Window settings for gating region n.',
   '$SMNO':' Specimen (e.g., tube) label.',
   '$SPILLOVER': 'Fluorescence spillover matrix.',
   '$SRC': 'Source of the specimen (patient name, cell types)',
   '$SYS': 'Type of computer and its operating system.',
   '$TIMESTEP': 'Time step for time parameter.',
   '$TR': 'Trigger, parameter and its threshold.',
   '$VOL': 'Volume of sample run during data acquisition.',
   '$WELLID': 'Well identifier.',
   }

RegexDescriptor = namedtuple('RegexDescriptor',['regex_string','keyword','regex'])
"""Store regular expressions that describe documented keywords"""

def _get_regexs(keywords):
   output = []
   for key in keywords:
      parts = key.split('n')
      regex = ('\d+'.join(parts)).replace('$','\$')+'$'
      output.append(RegexDescriptor(regex,key,re.compile(regex,re.IGNORECASE)))
   return output

class KeyWordDict:
   """A dictionary for accessing keywords that

   1. Preserves the original keywords
   2. Provides case-INSENSITIVE access to keywords as per the spec
   3. Does not allow empty strings as keywords or values
   """
   def __init__(self,kvs=[]):
       self._d = {} # dictionary keyed uppercase
       self._l = [] # list of original values in the order we recieve them
       self._uc_to_orig = {} #dictionary to convert upper case and original key format
       """Optionally initialize with an interable list of key-value pairs"""
       for kv in kvs:
          self._do_set(kv[0],kv[1])

   def keys(self): return self._l
   def __iter__(self):
      for k in self.keys(): yield k
   def __getitem__(self,key):
      uc = key.upper()
      if uc not in self._d: raise ValueError('key not in KeyWordDict')
      return self._d[uc]
   def __delitem__(self,key):
      uc = key.upper()
      if uc not in self._uc_to_orig:
         sys.stderr.write("Warning deleting a key not present in structure. nothing happens\n")
         return
      orig = self._uc_to_orig[uc]
      del self._uc_to_orig[uc]
      self._l.remove(orig)
      del self._d[uc]
   def __setitem__(self,key,value):
      if key == '': raise ValueError('Empty strings are not permitted for key value pairs')
      if value == '': raise ValueError('Empty strings are not permitted for key value pairs')
      self._do_set(key,value)

   def _do_set(self,key,value):
       #print('set item '+key+' '+str(value))
       uc = key.upper()
       if uc not in self._d:
          self._l.append(key)
       else:
          #sys.stderr.write("Warning repeat key. Overwrites values\n")
          ind = self._l.index(self._uc_to_orig[uc])
          self._l[ind] = key
       self._d[uc] = value
       self._uc_to_orig[uc] = key
   def __contains__(self,key):
      if key.upper() in self._d: return True
      return False

class Text(KeyWordDict):
   """Parse the TEXT portion of the file. Assumes that the header has
   been processed in set in self._header.

   In version 3.0 of the FCS specification, the TEXT must fit entirely
   in the first 99,999,999 bytes of data.

   Text object can be accessed as a dictionary, as it is composed of key/value
   pairs, but these will all be strings keys and string values.

   Can take an input data from an FCS file, but this object is mutable.
   """
   def __init__(self,data=None):
      self._delimiter = '/'
      if data:
         self._delimiter=chr(data[0])
         """If we have data, go ahead and initialize

         Decode keyword value pairs

         Tricky Regex for not getting escaped forward slashes"""
         not_single_slash = '(?:[^'+self._delimiter+']|'+self._delimiter*2+')+'
         prog = re.compile(self._delimiter+'('+not_single_slash+')'+self._delimiter+'('+not_single_slash+')')
         miter = prog.finditer(data.decode('utf-8'))
         """Bake removing the escape characters into generating the
         key value pairs

         Since keywords are case inssensitive, take them to uppercase,

         no mater what."""
         super().__init__([(m.group(1).replace(self._delimiter*2,self._delimiter).upper(),
                            m.group(2).replace(self._delimiter*2,self._delimiter)) for m in miter])
      else:
         """If no data start with an empty text field"""
         super().__init__([])
      return

   def __setitem__(self,key,value):
      super().__setitem__(key,value)

   @property
   def bytes(self):
      ostr = self._delimiter
      for key in self.keys():
         ostr+=key.replace(self._delimiter,self._delimiter*2)+self._delimiter\
              +self[key].replace(self._delimiter,self._delimiter*2)+self._delimiter
      return bytes(ostr.encode('utf-8'))

   def __str__(self):
      return self._data.decode('utf-8')

   def _get_documented_keys(self,keywords):
      """Return a dictionary keyed by optional keys with values being
      the keyword in the documentation

      input is a dictionary of keywords and their description from 
      the documentation
      """
      regexs = _get_regexs(keywords)
      output = {}
      """traverse the keys and look for ones with a maching regex"""
      for key in self.keys():
         v = [x.keyword for x in regexs if x.regex.match(key)]
         if len(v) > 0: output[key] = v[0]
      return output

   def get_required_keys(self):
      """Return a dictionary keyed by optional keys with values being
      the keyword in the documentation"""
      return self._get_documented_keys(_required_keywords.keys())

   def get_unset_required_keywords(self):
      """From keywords we know should be present... see if any are not there."""
      return list(set(_required_keywords.keys())-set(self.get_required_keys().values()))

   @property
   def has_required_keywords(self):
      """Members are present from all the required keywords"""
      if len(self.get_unset_required_keywords()) == 0: return True
      return False

   def get_optional_keys(self):
      """Return a dictionary keyed by optional keys with values being
      the keyword in the documentation"""
      return self._get_documented_keys(_optional_keywords.keys())

   def get_orphan_keys(self):
      s1 = set(set(_required_keywords.keys()) | \
          set(_optional_keywords.keys()))
      s2 = set(self.get_required_keys().values()) | \
           set(self.get_optional_keys().values())
      return list(set(s2)-set(s1))

   @property
   def parameters(self):
      n = int(self['$PAR'])
      return [Parameter(x,self) for x in range(1,n+1)]
