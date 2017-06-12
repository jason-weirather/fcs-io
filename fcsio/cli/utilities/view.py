""" View FCS file contents """

import argparse, sys, gzip, re, io
from fcsio import FCS

def main(args):
   """setup input and output handles"""
   inf = sys.stdin.buffer
   if args.input != '-':
      if args.input[-3:] == '.gz': inf = gzip.open(args.input,'rb')
      else: inf = open(args.input,'rb')
   fcs = FCS(inf.read())
   of = sys.stdout
   if args.output:
      if args.output[-3:] == '.gz': of = gzip.open(args.output,'w')
      else: of = open(args.output,'w')
   inf.close() # read the bytes and close inputs

   if not args.no_header:
      of.write("\t".join([x.short_name for x in fcs.parameters])+"\n")
   if args.R:
      of.close()
      return
   mat = fcs.data.matrix
   for row in mat:
      if args.simple:
         fstr = "{0:."+str(args.simple)+"f}"
         of.write("\t".join([fstr.format(x).rstrip('0').rstrip('.') for x in row])+"\n")
      else:
         of.write("\t".join([str(x) for x in row])+"\n")
   of.close()
def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Provide a description of the FCS file and its contents ",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   parser.add_argument('-s','--simple',action='store_const',const=2,help="decimal places in float")
   group1 = parser.add_mutually_exclusive_group()
   group1.add_argument('--no_header',action='store_true',help="Exclude the header in the output")
   group1.add_argument('-R',action='store_true',help="Only output the header")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
