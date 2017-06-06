""" Remove the parameters of an fcs file

You can **keep** specified parameter(s) if you use the ``--inv`` option.

"""

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

   inf.close()
   if args.inv:
      fcs.parameters = [x for x in fcs.parameters if x.short_name in args.short_names]
   else:
      fcs.parameters = [x for x in fcs.parameters if x.short_name not in args.short_names]
   of.write(fcs.output_constructor().fcs_bytes)

   of.close()
   return

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Remove the parameters from an FCS file",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   parser.add_argument('-n','--short_names',required=True,nargs='+',help="remove these parameters")
   parser.add_argument('-i','--inv',action='store_true',help="invert the filter to keep the parameter(s)")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
