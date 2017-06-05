""" Provide a description of the FCS file and its contents """

import argparse, sys, gzip, re, io, random
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

   cell_count = fcs.standard.TOT
   do_essential = args.essential==True
   if args.range is not None:
      f2 = fcs.filter.events(range(args.range[0]-1,args.range[1]))
      of.write(f2.construct_fcs(do_essential).fcs_bytes)
      of.close()
      return
   if args.random is not None:
      rset = list(range(0,fcs.standard.TOT))
      random.shuffle(rset)
      rset = sorted(rset[0:args.random])
      f2 = fcs.filter.events(rset)
      of.write(f2.construct_fcs(do_essential).fcs_bytes)
      of.close()
      return

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Provide a description of the FCS file and its contents ",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   parser.add_argument('--essential',action='store_true',help="Only output the essential parts.  Exclude OTHER fields.")
   group1 = parser.add_mutually_exclusive_group()
   group1.add_argument('--range',nargs=2,type=int,help="get events (cells) in this range (1 indexed)")
   group1.add_argument('--random',type=int,help="number of cells to randomly draw")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
