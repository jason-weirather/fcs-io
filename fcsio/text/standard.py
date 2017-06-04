class Standard:
   """ interact with text fields through standard key words,
   these EXCLUDE parameters which are available in 'parameter'

   .. warning:: While you may be able to read and alter parameters
                here, any byte ranges will hold very little meaning
                excpet when first read and describing an original file
                or after an output_constructor has been called and you
   """
   def __init__(self,text):
      self._text = text

   """Byte-offest to the beginning of the ANALYSIS segment"""
   @property
   def BEGINANALYSIS(self):
      return int(self._text['$BEGINANALYSIS'])
   @BEGINANALYSIS.setter
   def BEGINANALYSIS(self,val):
      self._text['$BEGINANALYSIS'] = int(val)

   """Byte-offset to the beginning of the DATA segment"""
   @property
   def BEGINDATA(self):
      return int(self._text['$BEGINDATA'])
   @BEGINDATA.setter
   def BEGINDATA(self,val):
      self._text['$BEGINDATA'] = int(val)

   """Byte-offset to the beginning of the TEXT segment"""
   @property
   def BEGINSTEXT(self):
      return int(self._text['$BEGINSTEXT'])
   @BEGINSTEXT.setter
   def BEGINSTEXT(self,val):
      self._text['$BEGINSTEXT'] = int(val)

   """Byte order for data acquisition computer"""
   @property
   def BYTEORD(self):
      if self._text['$BYTEORD'] == '1,2,3,4': return 'little endian'
      if self._text['$BYTEORD'] == '4,3,2,1': return 'big endian'
      raise ValueError("Unsupported byte order "+self._text['$BYTEORD'])
   @BYTEORD.setter
   def BYTEORD(self,val):
      """ Byte order must be 'little endian' or 'big endian'"""
      if val == 'little endian': self._text['$BYTEORD'] = '1,2,3,4'
      elif val == 'big endian': self._text['$BYTEORD'] = '4,3,2,1'
      else: ValueError("Must set BYTEORD to either 'little endian' or 'big endian'")

   """Type of data in the DATA segment"""
   @property
   def DATATYPE(self):
      return self._text['$DATATYPE']
   @DATATYPE.setter
   def DATATYPE(self,val):
      valid = ('I','F','D','A')
      if val not in valid: raise ValueError("DATATYPE "+val+" is not valid "+str(valid))
      self._text['$DATATYPE'] = val

   """Byte-offset to the end of the ANALYSIS segment"""
   @property
   def ENDANALYSIS(self):
      return int(self._text['$ENDANALYSIS'])
   @ENDANALYSIS.setter
   def ENDANALYSIS(self,val):
      self._text['$ENDDATA'] = int(val)

   """Byte-offset to the end of the DATA segment"""
   @property
   def ENDDATA(self):
      return int(self._text['$ENDDATA'])
   @ENDDATA.setter
   def ENDDATA(self,val):
      self._text['$ENDDATA'] = int(val)

   """Byte-offset to the end of the TEXT segment"""
   @property
   def ENDSTEXT(self):
      return int(self._text['$ENDSTEXT'])
   @ENDSTEXT.setter
   def ENDSTEXT(self,val):
      self._text['$ENDSTEXT'] = int(val)

   """Data mode. Everything except list is deprecated"""
   @property
   def MODE(self):
      return self._text['$MODE']
   @MODE.setter
   def MODE(self,val):
      if val != 'L': raise ValueError("Only 'L' mode is currently accetable")
      self._text['$MODE'] = val

   """Offset to the next data set in the file"""
   @property
   def NEXTDATA(self):
      return int(self._text['$NEXTDATA'])
   @NEXTDATA.setter
   def NEXTDATA(self,val):
      self._text['$NEXTDATA'] = int(val)

   """Number of parameters in an event"""
   @property
   def PAR(self):
      return len(self._text.parameter_data.keys())
   @PAR.setter
   def PAR(self,val):
      raise ValueError('modify PAR by changing paramaters')

   """Total number of events in the dataset"""
   @property
   def TOT(self):
      return int(self._text['$TOT'])
   @TOT.setter
   def TOT(self,val):
      raise ValueError('modify TOT by changing data property')
