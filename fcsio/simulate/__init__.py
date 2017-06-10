from fcsio import FCS, FCSOptions
import random

def simulate(number_of_events=10000,channels=5):
   """Take number of events and channels as inputs and
   output the FCS file bytes

   :param number_of_events: number of events
   :param channels: number of channels
   :type number_of_events: int
   :type channels: int
   :return: FCS file data
   :rtype: bytearray
   """
   fcs = FCS(fcs_options=FCSOptions())
   fcs.parameters.add('Time')
   fcs.parameters.add('Event_Length',index=1)
   for i in range(0,channels):
      fcs.parameters.add('Sim_'+str(i+1),index=len(fcs.parameters))

   mat = fcs.data.matrix
   numbers = []
   tarr = [i+1 for i in range(0,number_of_events)]
   numbers.append(tarr)
   larr = [random.gauss(50,10) for i in range(0,number_of_events)]
   numbers.append(larr)
   for i in range(0,channels):
      c = [random.gauss(50,10) if random.random() < 0.2 else random.gauss(80,20) for i in range(0,number_of_events)]
      c = [0 if x < 0 else x for x in c]
      numbers.append(c)
   for i in range(0,number_of_events):
      mat.append([0 for i in range(0,len(fcs.parameters))])
      for j in range(0,len(numbers)): mat[-1][j] = numbers[j][i]
   fcs.data.matrix = mat
   return fcs.output_constructor().fcs_bytes
