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
      """Get the byte offset for BEGINANALYSIS

      **Setter:** assign an `int` to the keyword

      :return: the BEGINANALYSIS value
      :rtype: int
      """
      return int(self._text['$BEGINANALYSIS'])
   @BEGINANALYSIS.setter
   def BEGINANALYSIS(self,val):
      self._text['$BEGINANALYSIS'] = int(val)

   """Byte-offset to the beginning of the DATA segment"""
   @property
   def BEGINDATA(self):
      """Get the byte offset for BEGINDATA

      **Setter:** assign an `int` to the keyword

      :return: the BEGINDATA value
      :rtype: int
      """
      return int(self._text['$BEGINDATA'])
   @BEGINDATA.setter
   def BEGINDATA(self,val):
      self._text['$BEGINDATA'] = int(val)

   """Byte-offset to the beginning of the TEXT segment"""
   @property
   def BEGINSTEXT(self):
      """Get the byte offset for BEGINTEXT supplemental text

      **Setter:** assign an `int` to the keyword

      :return: the BEGINTEXT value
      :rtype: int
      """
      return int(self._text['$BEGINSTEXT'])
   @BEGINSTEXT.setter
   def BEGINSTEXT(self,val):
      self._text['$BEGINSTEXT'] = int(val)

   """Byte order for data acquisition computer"""
   @property
   def BYTEORD(self):
      """Get the byte order type as either 'little endian' or 'big endian'

      **Setter:** set the key word from either 'little endian' or 'big endian' string

      :return: the BYTEORD description
      :rtype: string that is either 'little endian' or 'big endian'
      """
      if self._text['$BYTEORD'] == '1,2,3,4': return 'little endian'
      if self._text['$BYTEORD'] == '4,3,2,1': return 'big endian'
      raise ValueError("Unsupported byte order "+self._text['$BYTEORD'])
   @BYTEORD.setter
   def BYTEORD(self,val):
      """ Byte order must be 'little endian' or 'big endian'"""
      if val == 'little endian': self._text['$BYTEORD'] = '1,2,3,4'
      elif val == 'big endian': self._text['$BYTEORD'] = '4,3,2,1'
      else: ValueError("Must set BYTEORD to either 'little endian' or 'big endian'")

   @property
   def DATATYPE(self):
      """Type of the DATA in the data segment

      **Setter:** assign an `char` to the keyword

      :return: the DATATYPE
      :rtype: char
      """
      return self._text['$DATATYPE']
   @DATATYPE.setter
   def DATATYPE(self,val):
      valid = ('I','F','D','A')
      if val not in valid: raise ValueError("DATATYPE "+val+" is not valid "+str(valid))
      self._text['$DATATYPE'] = val

   """Byte-offset to the end of the ANALYSIS segment"""
   @property
   def ENDANALYSIS(self):
      """Get the byte offset for ENDANALYSIS

      **Setter:** assign an `int` to the keyword

      :return: the ENDANALYSIS value
      :rtype: int
      """
      return int(self._text['$ENDANALYSIS'])
   @ENDANALYSIS.setter
   def ENDANALYSIS(self,val):
      self._text['$ENDDATA'] = int(val)

   """Byte-offset to the end of the DATA segment"""
   @property
   def ENDDATA(self):
      """Get the byte offset for ENDDATA

      **Setter:** assign an `int` to the keyword

      :return: the ENDDATA value
      :rtype: int
      """
      return int(self._text['$ENDDATA'])
   @ENDDATA.setter
   def ENDDATA(self,val):
      self._text['$ENDDATA'] = int(val)

   """Byte-offset to the end of the TEXT segment"""
   @property
   def ENDSTEXT(self):
      """Get the byte offset for ENDSTEXT supplemental text

      **Setter:** assign an `int` to the keyword

      :return: the ENDSTEXT value
      :rtype: int
      """
      return int(self._text['$ENDSTEXT'])
   @ENDSTEXT.setter
   def ENDSTEXT(self,val):
      self._text['$ENDSTEXT'] = int(val)

   """Data mode. Everything except list is deprecated"""
   @property
   def MODE(self):
      """Get the MODE of data layout

      **Setter:** assign an `char` to the keyword

      :return: the MODE value
      :rtype: char
      """
      return self._text['$MODE']
   @MODE.setter
   def MODE(self,val):
      if val != 'L': raise ValueError("Only 'L' mode is currently accetable")
      self._text['$MODE'] = val

   """Offset to the next data set in the file"""
   @property
   def NEXTDATA(self):
      """Get the byte offset for NEXTDATA the next fcs data

      **Setter:** assign an `int` to the keyword

      :return: the NEXTDATA value
      :rtype: int
      """
      return int(self._text['$NEXTDATA'])
   @NEXTDATA.setter
   def NEXTDATA(self,val):
      self._text['$NEXTDATA'] = int(val)

   """Number of parameters in an event"""
   @property
   def PAR(self):
      """Get the number of parameters

      .. warning:: You cannot set the PAR, as it is infered from the parameters present

      :return: the PAR value
      :rtype: int
      """
      return len(self._text.parameter_data.keys())
   @PAR.setter
   def PAR(self,val):
      raise ValueError('modify PAR by changing paramaters')

   """Total number of events in the dataset"""
   @property
   def TOT(self):
      """Get the number of events

      .. warning:: You cannot set the TOT, as it is infered from the parameters present

      :return: the TOT value
      :rtype: int
      """
      return int(self._text['$TOT'])
   @TOT.setter
   def TOT(self,val):
      raise ValueError('modify TOT by changing data property')
