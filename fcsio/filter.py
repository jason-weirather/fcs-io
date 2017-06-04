from fcsio.text import get_required_keywords
class Filter:
   """ Filter an FCS class according by various options and output an FCS

   .. note:: This class is should be accessed through 
             the :class:`fcsio.FCS.filter` method.

   When filter is called, a copy is created of the FCS class 
   used to initialize it is generated. This copy is subsequenty
   modified as necessary in the filtering process.

   :param fcs: Start filtering from an FCS class.
   :type fcs: :class:`fcsio.FCS`
   """
   def __init__(self,fcs):
      self._fcs = fcs.copy()
   def none(self):
      return self._fcs
   def events(self,row_indecies):
      """Filter the events (or cells) by index.  This is to facilitate
      subsetting the data with random sampling.

      :param row_indecies: A list of indecies (0-indexed) of events to include
      :type row_indecies: list
      :return: A filtered FCS
      :rtype: :class:`fcsio.FCS`
      """
      filtered_matrix = [self._fcs.data.matrix[i] for i in row_indecies]
      self._fcs.data.matrix = filtered_matrix
      return self._fcs
   def gate(self,short_name,min=None,max=None):
      """Filter the FCS file based on values of a parameter

      include greater than or equal to min if set
      include less than or equal to max if set

      :param short_name: PnN short name
      :type short_name: string
      :param min: remove anything less than this
      :type min: float
      :param max: remove anything greater than this
      :type max: float
      """
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
      """Trim down the FCS to all but the minimal number of required fields

      by its very nagture this is a very lossy filter, but could concievably
      help with some memory issues that could come up.

      """

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
