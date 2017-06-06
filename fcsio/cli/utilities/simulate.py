""" Create a fake FCS data for testing purposes"""

import argparse, sys, gzip, re, io, random
from fcsio import FCS
from fcsio import FCSOptions

def main(args):
   """setup input and output handles"""
   of = sys.stdout.buffer
   if args.output:
      if args.output[-3:] == '.gz': of = gzip.open(args.output,'wb')
      else: of = open(args.output,'wb')


   fcs = FCS(fcs_options=FCSOptions())
   fcs.parameters.add('Time')
   fcs.parameters.add('Event_Length',index=1)
   for i in range(0,args.channels):
      fcs.parameters.add('Sim_'+str(i+1),index=len(fcs.parameters))

   mat = fcs.data.matrix
   numbers = []
   tarr = [i+1 for i in range(0,args.number_of_events)]
   numbers.append(tarr)
   larr = [random.gauss(50,10) for i in range(0,args.number_of_events)]
   numbers.append(larr)
   for i in range(0,args.channels):
      c = [random.gauss(50,10) if random.random() < 0.2 else random.gauss(80,20) for i in range(0,args.number_of_events)]
      c = [0 if x < 0 else x for x in c]
      numbers.append(c)
   for i in range(0,args.number_of_events):
      mat.append([0 for i in range(0,len(fcs.parameters))])
      # put in our data
      for j in range(0,len(numbers)): mat[-1][j] = numbers[j][i]
      #mat[-1][0] = i+1
      #mat[-1][1] = larr[i]
   fcs.data.matrix = mat
   of.write(fcs.output_constructor().fcs_bytes)
   of.close()
   return

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Access user-defined OTHER data from an fcs file",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   parser.add_argument('-n','--number_of_events',type=int,default=10000,help="Number of events to add")
   parser.add_argument('-c','--channels',type=int,default=5,help="Number of data channels")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
