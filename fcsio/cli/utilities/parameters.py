""" Access metadata on parameters from an fcs file """

import argparse, sys, gzip, re, io
from fcsio import FCS
from fcsio.cytof import FCS as FCS_CyTOF

def main(args):
   """setup input and output handles"""
   inf = sys.stdin.buffer
   if args.input != '-':
      if args.input[-3:] == '.gz': inf = gzip.open(args.input,'rb')
      else: inf = open(args.input,'rb')
   fcs = None
   if args.cytof:
      fcs = FCS_CyTOF(inf.read())
   else:
      fcs = FCS(inf.read())
   of = sys.stdout
   if args.output:
      if args.output[-3:] == '.gz': of = gzip.open(args.output,'w')
      else: of = open(args.output,'w')
   inf.close() # read the bytes and close inputs

   if not args.no_header:
      basic = '$PnN'+"\t"+'$PnS'
      of.write(basic)
      of.write("\n")
      #of.write("\t".join([x.short_name for x in fcs.parameters])+"\n")
   for param in fcs.parameters:
      of.write(param.short_name+"\t"+(param.long_name if param.long_name else ''))
      of.write("\n")
   #of.write(str(fcs.cytof.fcsheaderschema))

   if args.R:
      of.close()
      return
   of.close()

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Provide a description of the FCS file and its contents ",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   parser.add_argument('--cytof',action='store_true',help="FCS file has CyTOF data embedded")
   group = parser.add_mutually_exclusive_group()
   group.add_argument('--no_header',action='store_true',help="Don't describe the metafile header")
   group.add_argument('-R',action='store_true',help="Only output the header of the metadata")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
