""" Convert a tsv file into an FCS file 

Default will look for a header, you can set ``--no_header`` 
to change this behavior

"""

import argparse, sys, gzip, re, io
from fcsio import FCS
from fcsio import FCSOptions

def main(args):
   """setup input and output handles"""
   inf = sys.stdin.buffer
   if args.input != '-':
      if args.input[-3:] == '.gz': inf = gzip.open(args.input,'rb')
      else: inf = open(args.input,'rb')
   of = sys.stdout.buffer
   if args.output:
      if args.output[-3:] == '.gz': of = gzip.open(args.output,'wb')
      else: of = open(args.output,'wb')

   bare_bones = FCS(fcs_options=FCSOptions())
   inmat = []
   header = []
   if not args.no_header: 
      header = inf.readline()
      if not header: raise ValueError("empty input. Cant make an empty FCS file")
      header = header.decode("utf-8").rstrip().split("\t")
   for line in inf:
      inmat.append([float(x) for x in line.decode("ascii").rstrip().split("\t")])
   inf.close() # read the bytes and close inputs
   if len(inmat)==0: raise ValueError("empty fcs file, not supported")
   # if no header, make a fake one
   if args.no_header:
      header = ['Param_'+str(i+1) for i in range(0,len(inmat[0]))]
   for param in header:
      bare_bones.parameters.add(param,index=len(bare_bones.parameters))
   bare_bones.data.matrix = inmat
   of.write(bare_bones.output_constructor().fcs_bytes)
   of.close()
   return

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Convert a TSV file with parameter columns into an FCS file ",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   parser.add_argument('--no_header',action='store_true',help="You are not specifying a header so give generic parameter labels i.e. Param_1, Param_2, etc..")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
