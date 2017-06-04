import re, sys, json

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

class Parameters:
   """class to access and modify the parameters defined by the
   TEXT segement with data stored in the DATA segement

   input values are usually accessed through FCS properties

   :param text: the text object associated with an FCS object
   :param data: the data object associated iwth an FCS object
   :type text: :class:`fcsio.text.Text`
   :type data: :class:`fcsio.data.Data`
   """
   def __init__(self,text,data):
      self._text = text
      self._data = data
      #self._parameters = [Parameter(i,self._text.parameter_data) for i in range(1,int(self._text['$PAR']))]
   @property
   def parameters(self):
      """ Return the list of paremeters as Parameter objects

      :return: parameters
      :rtype: list of :class:`fcsio.test.parameters.Parameter`
      """
      #return [Parameter(i,self._text.parameter_data) for i in range(1,int(self._text['$PAR']))]
      return [Parameter(i,self._text.parameter_data) for i in sorted(self._text.parameter_data)]
   def __iter__(self):
      for p in self.parameters:
         yield p
   def indexOf(self,short_name=None):
      """Get the index in a list of parameters according to a short_name of a parameter

      :param short_name: the PnN short name
      :type short_name: string
      :return: get he index of the short name
      :rtype: int
      """
      if short_name is not None:
         return [x.short_name for x in self.parameters].index(short_name)
      return None
   def delete(self,short_names=[]):
      """Remove a list of parameters defined by the list of short names

      :param short_names: the PnP short names as a list
      :type short_name: list of strings
      """
      removed_indecies = []
      for short_name in short_names:
         for p in self.parameters:
            if p.short_name != short_name: continue
            """ delete this parameter"""
            index = p.index
            del self._text.parameter_data[index]
            removed_indecies.append(index)
      filtered_matrix = []
      for row in self._data.matrix:
         """ drop columns that were dropped """
         filtered_matrix.append(row)
         if len(row) < 48:
            print(len(row))
         #print('rowlen '+str(len(new_row)))
      self._data.matrix = filtered_matrix

class Parameter:
   """A class defining a single Parameter. These are attributes
   being recorded by the machine for each event, and they come with
   a number of keywords describing each one.

   :param i: index of the parameter (0-indexed)
   :param pdata: The dict keyed by index, then generic parameter keyword accessible through :class:`fcsio.text.Text`
   :type i: int
   :type pdata: dict

   .. note:: Can be accessed as a dictionary by keyword.  Use get_keywords()
             to get available keywords, e.g. '$PnS'

   """
   def __init__(self,i,pdata):
      self._pdata = pdata
      self._i = i
   @property
   def index(self):
      """get the 0-indexed order number of the parameter
      :return: index (0-based)
      :rtype: int
      """
      return self._i
   @property
   def bits(self):
      """$PnB attribute for this parameter

      **REQUIRED ATTRIBUTE**

      Please keep in mind that bits is required to be 32 for type F.
      If $DATATYPE is F this will represent the number of characters
      for each data value

      **Setter:** assign an `int` to $PnB

      :return: $PnB
      :rtype: int
      """
      if '$PnB' not in self._pdata[self._i]: return None
      return int(self._pdata[self._i]['$PnB'])
   @bits.setter
   def bits(self,val):
      self._pdata[self._i]['$PnB'] = str(val)
   @property
   def amplification_type(self):
      """$PnE attribute for this paramete.

      **REQUIRED ATTRIBUTE**

      Specifies whether the the parameter data is stored on linear or
      logarithmic scale.  For a linear scale, (0,0) will be used.
      When floating point storage is used, this linear scale will be used

      Here it returns as a tuple pair of floats
      and the first float is the number of log decades and the second is
      the linear value that would have a log value of 0

      .. note:: Can be converted with the formula 10^(f1*xc/r))*f2 where
                xc is the channel value.

      **Setter:** assign an `(float1,float2)` to $PnE

      :return: $PnE
      :rtype: (`float`,`float`)
      """
      s = self._pdata[self._i]['$PnE'].split(',')
      return (float(s[0]),float(s[1]))
   @amplification_type.setter
   def amplification_type(self,tup):
      self._pdata[self._i]['$PnE'] = str(tup[0])+','+str(tup[1])
   @property
   def short_name(self):
      """$PnN short name attribute for this parameter

      **REQUIRED ATTRIBUTE**

      **Setter:** assign a `string` to $PnN

      :return: $PnN
      :rtype: string
      """
      return self._pdata[self._i]['$PnN']
   @short_name.setter
   def short_name(self,val):
      self._pdata[self._i]['$PnN'] = val
   @property
   def range(self):
      """$PnR max range attribute for this parameter

      **REQUIRED ATTRIBUTE**

      Holds the maximum value that data for this parameter can reach.
      The value stored can exceed the true max.

      **Setter:** assign an `int` to $PnR

      :return: $PnR
      :rtype: int
      """
      return int(self._pdata[self._i]['$PnR'])
   @range.setter
   def range(self,val):
      self._pdata['$PnR'] = str(val)

   # begin optional values
   @property
   def calibration(self):
      """$PnCALIBRATION short name attribute for this parameter

      Parameter has 1 per `float` scale units.

      **Setter:** assign a tuple (`float`,`string`) to $PnCALIBRATION

      :return: $PnCALIBRATION
      :rtype: (`float`,`string`) or `None`
      """
      k = '$PnCALIBRATION'
      if k not in self._pdata[self._i]: return None
      v = self._pdata[self._i][k]
      m - re.match('([^,]+),(.*)$',v)
      return (float(m.group(1)),float(m.group(2)))
   @calibration.setter
   def calibration(self,tup):
      self._pdata['$PnCALIBRATION'] = str(tup[0])+','+tup[1]
   @property
   def visualization_scale(self):
      """$PnD short name attribute for this parameter

      visualization scale recommendations for parameter

      **Setter:** assign a tuple (`string`,`float`,`float`) to $PnD

      :return: $PnD
      :rtype: (`string`,`float`,`float`) or `None`
      """
      k = '$PnD'
      if k not in self._pdata[self._i]: return None
      v = self._pdata[self._i][k]
      m - re.match('^(.*),([^,]+),([^,]+])$',v)
      return (m.group(1),float(m.group(2)),float(m.group(3)))
   @visualization_scale.setter
   def visualization_scale(self,tup):
      self._pdata[self._i]['$PnD'] = tup[0]+','+str(tup[1])+','+str(tup[2])
   @property
   def optical_filter(self):
      """$PnF optical filter attribute for this parameter

      **Setter:** assign a `string` to $PnF

      :return: $PnF
      :rtype: string or `None`
      """
      k = '$PnF'
      if k not in self._pdata[self._i]: return None
      return self._pdata[self._i][k]
   @optical_filter.setter
   def optical_filter(self,val):
      self._pdata[self._i]['$PnF'] = val
   @property
   def amplification_gain(self):
      """$PnG gain used to amplify the value of this parameter

      **Setter:** assign a `float` to $PnG

      :return: $PnG
      :rtype: float or `None`
      """
      k = '$PnG'
      if k not in self._pdata[self._i]: return None
      return float(self._pdata[self._i][k])
   @amplification_gain.setter
   def amplification_gain(self,val):
      self._pdata[self._i]['$PnG'] = str(val)
   @property
   def excitation_wavelengths(self):
      """$PnL excitation wavelength(s) for parameter N

      **Setter:** assign a list of ints to $PnL

      :return: $PnL
      :rtype: list of ints or `None`
      """
      k = '$PnL'
      if k not in self._pdata[self._i]: return None
      s = self._pdata[self._i][k].split(',')
      return [int(x) for x in x]
   @excitation_wavelengths.setter
   def excitation_wavelengths(self,arr):
      self._pdata[self._i]['$PnL'] = ','.join([str(x) for x in arr])
   @property
   def excitation_power(self):
      """$PnO power of lightsource in mW used to excite the parameter

      **Setter:** assign an `int` to $PnO

      :return: $PnO
      :rtype: int or `None`
      """
      k = '$PnO'
      if k not in self._pdata[self._i]: return None
      return int(self._pdata[self._i][k])
   @excitation_power.setter
   def excitation_power(self,val):
      self._pdata[self._i]['$PnO'] = str(val)
   @property
   def emitted_light(self):
      """$PnP amount of light collected by dector for a parmeter as a
         percentage of emitted light

      **Setter:** assign an `int` to $PnP

      :return: $PnP as an integer percent
      :rtype: int or `None`
      """
      k = '$PnP'
      if k not in self._pdata[self._i]: return None
      return int(self._pdata[self._i][k])
   @emitted_light.setter
   def emitted_light(self,val):
      self._pdata[self._i]['$PnP'] = str(val)
   @property
   def long_name(self):
      """$PnS defines a long name for the parameter

      **Setter:** assign a `string` to $PnS

      :return: $PnS long name
      :rtype: string or `None`
      """
      k = '$PnS'
      if k not in self._pdata[self._i]: return None
      return self._pdata[self._i][k]
   @long_name.setter
   def long_name(self,val):
      self._pdata[self._i]['$PnS'] = val
   @property
   def detector_type(self):
      """$PnT detector type for this parameter

      **Setter:** assign a `string` to $PnT

      :return: $PnT
      :rtype: string or `None`
      """
      k = '$PnT'
      if k not in self._pdata[self._i]: return None
      return self._pdata[self._i][k]
   @detector_type.setter
   def detector_type(self,val):
      self._pdata[self._i]['$PnT'] = val
   @property
   def detector_voltage(self):
      """$PnV detector voltage for the parameter measured in volts

      **Setter:** assign a `float` to $PnV

      :return: $PnV
      :rtype: float or `None`
      """
      k = '$PnV'
      if k not in self._pdata[self._i]: return None
      return float(self._pdata[self._i][k])
   @detector_type.setter
   def detector_voltage(self,val):
      self._pdata[self._i]['$PnV'] = str(val)
   def get_keywords(self):
      """Get all the keywords available for this parameter

      :return: keywords available
      :rtype: `list` of strings
      """
      return self._pdata[self._i].keys()
   def keys(self):
      """an alias for get_keywords

      :alsosee: :class:`fcsio.text.parameters.Parameter.get_keywords`
      """
      return self.get_keywords()
   def __getitem__(self,key):
      return self._pdata[self._i][key]
   def __delitem(self,keyword):
      del self._pdata[self._i][keyword]
