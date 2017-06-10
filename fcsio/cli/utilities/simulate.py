""" Create a fake FCS data for testing purposes"""

import argparse, sys, gzip, re, io
from fcsio.simulate import simulate

def _main(args):
   """setup input and output handles"""
   of = sys.stdout.buffer
   if args.output:
      if args.output[-3:] == '.gz': of = gzip.open(args.output,'wb')
      else: of = open(args.output,'wb')
   of.write(simulate(args.number_of_events,args.channels))
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
   """function for calling program by command through a function

   :param cmd: the command broken apart as a list
   :type cmd: list
   """
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   _main(args)
   sys.argv = cache_argv
