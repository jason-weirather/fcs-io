""" Read the OTHER user defined segments from a file """

import argparse, sys, gzip, re, io
from fcsio import FCS

def main(args):
   """setup input and output handles"""
   inf = sys.stdin.buffer
   if args.input != '-':
      if args.input[-3:] == '.gz': inf = gzip.open(args.input,'rb')
      else: inf = open(args.input,'rb')
   fcs = FCS(inf.read())
   of = sys.stdout.buffer
   if args.output:
      if args.output[-3:] == '.gz': of = gzip.open(args.output,'wb')
      else: of = open(args.output,'wb')
   inf.close() # read the bytes and close inputs

   if len(fcs.other)==0:
      raise ValueError("Index for OTHER segment is out of range.  No other segment exists.")
   if args.segment_number > len(fcs.other):
      raise ValueError("Index for segment number is out of range, please choose an OTHER segement between (and including) 1 and "+str(len(fcs.other)))
   of.write(fcs.other[args.segment_number-1])

   of.close()
   return

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Reorder the parameters of an FCS file",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   parser.add_argument('-n','--segment_number',type=int,required=True,help="Segment number (starting at 1)")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
