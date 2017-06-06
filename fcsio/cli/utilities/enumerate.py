""" Add a parameter to enumerate data """

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

   if args.short_name in [x.short_name for x in fcs.parameters]:
      raise ValueError("you cant add duplicate short names: "+args.short_name)

   fcs.parameters.add(args.short_name,index=args.index)

   j = fcs.parameters.indexOf(args.short_name)
   mat = fcs.data.matrix
   i = 0
   for row in mat:
      i += 1
      if args.label is not None:
         row[j] = args.label
      elif args.auto_number:
         row[j] = i
   of.write(fcs.output_constructor().fcs_bytes)

   of.close()
   return

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Add a parameter to enumerate the data",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   parser.add_argument('-n','--short_name',required=True,help="The short name to give this")
   parser.add_argument('-i','--index',type=int,default=0,help="index to add the enumeration 0-before first to N, after the Nth parameter")
   group = parser.add_mutually_exclusive_group()
   group.add_argument('-a','--auto_number',action='store_true',help="The default is to auto_number")
   group.add_argument('--label',type=float,help="add a numeric label")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
