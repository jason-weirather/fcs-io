import re, sys, json

class Parameter:
   def __init__(self,i,text):
      self._text = text
      self._i = i
      return
   @property
   def _dict(self):
      o = {'bits': self.bits,
           'amplification_type': self.amplification_type,
           'short_name': self.short_name,
           'range': self.range,
          }
      return o
   def __str__(self):
      return json.dumps(self._dict)
   @property
   def index(self):
      return self._i
   @property
   def bits(self):
      return int(self._text['$P'+str(self._i)+'B'])
   @bits.setter
   def bits(self,val):
      self._text['$P'+str(self._i)+'B'] = str(val)
   @property
   def amplification_type(self):
      s = self._text['$P'+str(self._i)+'E'].split(',')
      return (float(s[0]),float(s[1]))
   @amplification_type.setter
   def amplification_type(self,tup):
      self._text['$P'+str(self._i)+'E'] = str(tup[0])+','+str(tup[1])
   @property
   def short_name(self):
      return self._text['$P'+str(self._i)+'N']
   @short_name.setter
   def short_name(self,val):
      self._text['$P'+str(self._i)+'N'] = val
   @property
   def range(self):
      return int(self._text['$P'+str(self._i)+'R'])
   @range.setter
   def range(self,val):
      self._text['$P'+str(self._i)+'R'] = str(val)

   # begin optional values
   @property
   def calibration(self):
      k = '$P'+str(self._i)+'CALIBRATION'
      if k not in self._text: return None
      return self._text[k]
   @calibration.setter
   def calibration(self,val):
      self._text['$P'+str(self._i)+'CALIBRATION'] = val
   @property
   def visualization_scale(self):
      k = '$P'+str(self._i)+'D'
      if k not in self._text: return None
      return self._text[k]
   @visualization_scale.setter
   def visualization_scale(self,val):
      self._text['$P'+str(self._i)+'D'] = val
   @property
   def optical_filter(self):
      k = '$P'+str(self._i)+'F'
      if k not in self._text: return None
      return self._text[k]
   @optical_filter.setter
   def optical_filter(self,val):
      self._text['$P'+str(self._i)+'F'] = val
   @property
   def amplification_gain(self):
      k = '$P'+str(self._i)+'G'
      if k not in self._text: return None
      return float(self._text[k])
   @amplification_gain.setter
   def amplification_gain(self,val):
      self._text['$P'+str(self._i)+'G'] = str(val)
   @property
   def excitation_wavelength(self):
      k = '$P'+str(self._i)+'L'
      if k not in self._text: return None
      s = self._text[k].split(',')
      return [int(x) for x in x]
   @excitation_wavelength.setter
   def excitation_wavelength(self,arr):
      self._text['$P'+str(self._i)+'L'] = ','.join([str(x) for x in arr])
   @property
   def excitation_power(self):
      k = '$P'+str(self._i)+'O'
      if k not in self._text: return None
      return int(self._text[k])
   @excitation_power.setter
   def excitation_power(self,val):
      self._text['$P'+str(self._i)+'O'] = str(val)
   @property
   def emitted_light(self):
      k = '$P'+str(self._i)+'P'
      if k not in self._text: return None
      return int(self._text[k])
   @emitted_light.setter
   def emitted_light(self,val):
      self._text['$P'+str(self._i)+'P'] = str(val)
   @property
   def name(self):
      k = '$P'+str(self._i)+'S'
      if k not in self._text: return None
      return self._text[k]
   @name.setter
   def name(self,val):
      self._text['$P'+str(self._i)+'S'] = val
   @property
   def detector_type(self):
      k = '$P'+str(self._i)+'T'
      if k not in self._text: return None
      return self._text[k]
   @detector_type.setter
   def detector_type(self,val):
      self._text['$P'+str(self._i)+'T'] = val
   @property
   def detector_voltage(self):
      k = '$P'+str(self._i)+'V'
      if k not in self._text: return None
      return float(self._text[k])
   @detector_type.setter
   def detector_voltage(self,val):
      self._text['$P'+str(self._i)+'V'] = str(val)

