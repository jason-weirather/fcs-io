""" Concatonate multiple FCS files intersecting on short names 
of parameters"""

import argparse, sys, gzip, re, io
from fcsio import FCS

def main(args):
   """setup input and output handles"""
   # make sure theres only one stdin at most
   if len([x for x in args.input if x == '-']) > 1:
      raise ValueError("cannot use stdin - multiple times")
   of = sys.stdout.buffer
   if args.output:
      if args.output[-3:] == '.gz': of = gzip.open(args.output,'wb')
      else: of = open(args.output,'wb')
   fcs_files = [FCS(get_handle(x).read()) for x in args.input]
   fcs = fcs_files[0]
   others = []
   if len(fcs_files) > 1:
      others = fcs_files[1:]
   # get the intersection of parameters
   intersect = set([x.short_name for x in fcs.parameters])
   for other in others:
      intersect = set([x.short_name for x in other.parameters]).intersection(intersect)
   if len(intersect) == 0:
      raise ValueError('no common short names')
   # now go through and subset our parameters to these starting with the main
   fcs.parameters = [x for x in fcs.parameters if x.short_name in intersect]
   short_names = [x.short_name for x in fcs.parameters]
   mat = fcs.data.matrix
   for other in others:
      reindexed = [other.parameters.indexOf(short_name) for short_name in short_names]
      ps = list([x for x in other.parameters])
      other.parameters = [ps[i] for i in reindexed]
      # now other is properly ordered
      omat = other.data.matrix
      for row in omat:
         mat.append(row)
   fcs.data.matrix = mat
   of.write(fcs.output_constructor().fcs_bytes)
   #[x.close() for x in handles] # read the bytes and close inputs
   of.close()
   return

def get_handle(val):
   inf = sys.stdin.buffer
   if val != '-':
      if val[-3:] == '.gz': inf = gzip.open(val,'rb')
      else: inf = open(val,'rb')
   return inf

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Concatonate multiple FCS files",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',nargs='+',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
