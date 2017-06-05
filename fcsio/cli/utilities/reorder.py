""" Reorder the parameters of an fcs file """

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

   ps = None
   if args.short_name:
      ps = sorted(fcs.parameters,key=lambda x: x.short_name)
   elif args.custom:
      temp = list([x for x in fcs.parameters])
      ps = [temp[int(re.match('(\d+)',x).group(1))-1] for x in args.custom.split(',')]
   else:
      ps = list([x for x in fcs.parameters])
   #check for reverse
   if args.reverse: ps = ps[::-1]

   fcs.parameters = ps
   of.write(fcs.output_constructor().fcs_bytes)

   of.close()
   return

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Reorder the parameters of an FCS file",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   group1 = parser.add_mutually_exclusive_group()
   group1.add_argument('--short_name',action='store_true',help="Only output required fields.  Exclude OTHER fields.")
   group1.add_argument('--custom',metavar=('index_list'),help="comma separated list of indecies (1-indexed)")
   parser.add_argument('-r','--reverse',action='store_true',help="reverse the order. can be called with other filters")
   args = parser.parse_args()
   try:
      if args.custom: 
         matches = [re.match('\d+$',x) for x in args.custom.split(',')]
         if len(matches) == 0:
            parser.error("need something here")
         for m in matches:
            if not m: parser.error("must be integer indecies in csv list")
   except:
      parser.error("must be integer indecies in csv") 
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
