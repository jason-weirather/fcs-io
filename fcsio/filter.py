from fcsio.text import get_required_keywords
class Filter:
   """ Filter an FCS class according by various options and output an FCS """
   def __init__(self,fcs):
      self._fcs = fcs.copy()
   def none(self):
      return self._fcs
   def cells(self,row_indecies):
      filtered_matrix = [self._fcs.data.matrix[i] for i in row_indecies]
      self._fcs.data.matrix = filtered_matrix
      return self._fcs
   def gate(self,short_name,min=None,max=None):
      #include greater than or equal to min if set
      #include less than or equal to max if set
      index = self._fcs.parameters.indexOf(short_name=short_name)
      mat = []
      for row in self._fcs.data.matrix:
         exclude = False
         if min is not None:
            if row[index] < min: exclude = True
         if max is not None:
            if row[index] > max: exclude = True
         if not exclude: mat.append(row)
      self._fcs.data.matrix = mat
      return self._fcs
   def parameters(self,short_names=None):
      #if short_names is None: return self._fcs
      return self._fcs
   def minimize(self):
      """Trim down self._fcs to all but the essentials"""

      """eliminate OTHER fields"""
      self._fcs._other = []

      """eliminate non required keywords"""
      rk = set(list(get_required_keywords().keys()))
      present_keys = list(self._fcs.text.keys())
      for k in present_keys:
         if k.upper() not in rk:
            del self._fcs.text[k.upper()]

      """eliminate non required parameter properties"""
      rk = set(list(get_required_keywords().keys()))
      for i in self._fcs.text.parameter_data:
         for k in list(self._fcs.text.parameter_data[i].keys()):
            if k not in rk: del self._fcs.text.parameter_data[i][k]
      return self._fcs
