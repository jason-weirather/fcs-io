""" Apply various filters to the FCS file """

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


   # BEGIN FILTERS
   f2 = None # will be set in the filter of choice

   if args.essential:
      f2 = fcs.filter.minimize()

   elif args.event_range:
      f2 = fcs.filter.events(range(args.event_range[0]-1,args.event_range[1]))

   elif args.event_downsample_random is not None:
      rset = list(range(0,fcs.standard.TOT))
      random.shuffle(rset)
      rset = sorted(rset[0:args.random])
      f2 = fcs.filter.events(rset)

   elif args.gate:
      if args.gate not in [p.short_name for p in fcs.parameters]:
          raise ValueError("you chose a gate not in parameters. available gates are: "+str([p.short_name for p in fcs.parameters]))
      f2 = fcs.filter.gate(args.gate,min=args.min,max=args.max)

   else:
      f2 = fcs.filter.none()

   # END FILTERS

   of.write(f2.output_constructor(args.strip==True).fcs_bytes)
   of.close()
   return

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Provide a description of the FCS file and its contents ",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   parser.add_argument('--strip',action='store_true',help="strip away OTHER data segments from the object")
   group1 = parser.add_mutually_exclusive_group()
   parser.add_argument('--essential',action='store_true',help="Only output required fields.  Exclude OTHER fields.")
   group1.add_argument('--event_range',nargs=2,type=int,help="get events (cells) in this range (1 indexed)")
   group1.add_argument('--event_downsample_random',type=int,help="number of cells to randomly draw")
   group1.add_argument('--gate',metavar='short_name',help="gate on short name. use min and max to define range")
   parser.add_argument('--min',type=float,help="Remove events less than this number")
   parser.add_argument('--max',type=float,help="Remove events greater than this")
   args = parser.parse_args()
   if (args.min is None and args.max is None) and args.gate:
      parser.error("if you gate you must set --min or --max")
   if (args.min is not None or args.max is not None) and not args.gate:
      parser.error("if you set a min or a max you must set a gate")
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
