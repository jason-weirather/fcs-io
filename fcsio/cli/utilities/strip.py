""" Remove general features like OTHER segements from an FCS file """

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

   f2 = None # will be set in the filter of choice
   if args.essential:
      f2 = fcs.filter.minimize()
   else: f2 = fcs.filter.none()

   of.write(f2.output_constructor(True).fcs_bytes)
   of.close()
   return

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Strip OTHER fields from the fcs file or more depending on options",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   parser.add_argument('--essential',action='store_true',help="Only output required fields.")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
