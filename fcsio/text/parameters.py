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
   TEXT segement with data stored in the DATA segement"""
   def __init__(self,text,data):
      self._text = text
      self._data = data
      #self._parameters = [Parameter(i,self._text.parameter_data) for i in range(1,int(self._text['$PAR']))]
   @property
   def parameters(self):
      #return [Parameter(i,self._text.parameter_data) for i in range(1,int(self._text['$PAR']))]
      return [Parameter(i,self._text.parameter_data) for i in sorted(self._text.parameter_data)]
   def __iter__(self):
      for p in self.parameters:
         yield p
   def indexOf(self,short_name=None):
      if short_name is not None:
         return [x.short_name for x in self.parameters].index(short_name)
      return None
   def delete(self,short_names=[]):
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
   def __init__(self,i,pdata):
      self._pdata = pdata
      self._i = i
   #@property
   #def _dict(self):
   #   o = {'bits': self.bits,
   #        'amplification_type': self.amplification_type,
   #        'short_name': self.short_name,
   #        'range': self.range,
   #       }
   #   return o
   #def __str__(self):
   #   return json.dumps(self._dict)
   @property
   def index(self):
      return self._i
   @property
   def bits(self):
      if '$PnB' not in self._pdata[self._i]: return None
      return int(self._pdata[self._i]['$PnB'])
   @bits.setter
   def bits(self,val):
      self._pdata[self._i]['$PnB'] = str(val)
   @property
   def amplification_type(self):
      s = self._pdata[self._i]['$PnE'].split(',')
      return (float(s[0]),float(s[1]))
   @amplification_type.setter
   def amplification_type(self,tup):
      self._pdata[self._i]['$PnE'] = str(tup[0])+','+str(tup[1])
   @property
   def short_name(self):
      return self._pdata[self._i]['$PnN']
   @short_name.setter
   def short_name(self,val):
      self._pdata[self._i]['$PnN'] = val
   @property
   def range(self):
      return int(self._pdata[self._i]['$PnR'])
   @range.setter
   def range(self,val):
      self._pdata['$PnR'] = str(val)

   # begin optional values
   @property
   def calibration(self):
      k = '$PnCALIBRATION'
      if k not in self._pdata[self._i]: return None
      return self._pdata[self._i][k]
   @calibration.setter
   def calibration(self,val):
      self._pdata['$PnCALIBRATION'] = val
   @property
   def visualization_scale(self):
      k = '$PnD'
      if k not in self._pdata[self._i]: return None
      return self._pdata[self._i][k]
   @visualization_scale.setter
   def visualization_scale(self,val):
      self._pdata[self._i]['$PnD'] = val
   @property
   def optical_filter(self):
      k = '$PnF'
      if k not in self._pdata[self._i]: return None
      return self._pdata[self._i][k]
   @optical_filter.setter
   def optical_filter(self,val):
      self._pdata[self._i]['$PnF'] = val
   @property
   def amplification_gain(self):
      k = '$PnG'
      if k not in self._pdata[self._i]: return None
      return float(self._pdata[self._i][k])
   @amplification_gain.setter
   def amplification_gain(self,val):
      self._pdata[self._i]['$PnG'] = str(val)
   @property
   def excitation_wavelength(self):
      k = '$PnL'
      if k not in self._pdata[self._i]: return None
      s = self._pdata[self._i][k].split(',')
      return [int(x) for x in x]
   @excitation_wavelength.setter
   def excitation_wavelength(self,arr):
      self._pdata[self._i]['$PnL'] = ','.join([str(x) for x in arr])
   @property
   def excitation_power(self):
      k = '$PnO'
      if k not in self._pdata[self._i]: return None
      return int(self._pdata[self._i][k])
   @excitation_power.setter
   def excitation_power(self,val):
      self._pdata[self._i]['$PnO'] = str(val)
   @property
   def emitted_light(self):
      k = '$PnP'
      if k not in self._pdata[self._i]: return None
      return int(self._pdata[self._i][k])
   @emitted_light.setter
   def emitted_light(self,val):
      self._pdata[self._i]['$PnP'] = str(val)
   @property
   def name(self):
      k = '$PnS'
      if k not in self._pdata[self._i]: return None
      return self._pdata[self._i][k]
   @name.setter
   def name(self,val):
      self._pdata[self._i]['$PnS'] = val
   @property
   def detector_type(self):
      k = '$PnT'
      if k not in self._pdata[self._i]: return None
      return self._pdata[self._i][k]
   @detector_type.setter
   def detector_type(self,val):
      self._pdata[self._i]['$PnT'] = val
   @property
   def detector_voltage(self):
      k = '$PnV'
      if k not in self._pdata[self._i]: return None
      return float(self._pdata[self._i][k])
   @detector_type.setter
   def detector_voltage(self,val):
      self._pdata[self._i]['$PnV'] = str(val)
   def get_keywords(self):
      return self._pdata[self._i].keys()
   def __getitem__(self,key):
      return self._pdata[self._i][key]
