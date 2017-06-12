""" Access metadata on parameters from an fcs file """

import argparse, sys, gzip, re, io, functools
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

   if args.cytof:
     # If its CyTOF we can just do it with that
     short_names = [x.short_name for x in fcs.parameters]
     meta = fcs.cytof.fcsheaderschema
     cols = meta.data['SegmentColumns']
     vs = []
     for col in cols:
        short_name = col['ColumnName']
        long_name = None
        m = re.match('(\S+)\(([^\)]+)\)$',col['ColumnName'])
        if m:
           short_name = m.group(2)
           long_name = m.group(1)
        vs.append([short_name,long_name,col['ColumnName']])
     cdata = {}
     for v in vs:
        if v[0] not in short_names: continue
        cdata[v[0]] = {'long_name':v[1],'ColumnName':v[2]}
     #Do analysis analytes
     for short_name in cdata:
        additional = [x for x in meta.data['AnalysisAnalytes'] if x['LabelName'] == cdata[short_name]['long_name']]
        if len(additional) > 0: additional = additional[0]
        else: additional = {}
        for k in additional: cdata[short_name]['AnalysisAnalytes-'+k] = additional[k]
     #Do aquasition analytes
     for short_name in cdata:
        additional = [x for x in meta.data['AcquisitionAnalytes'] if x['LabelName'] == cdata[short_name]['long_name']]
        if len(additional) > 0: additional = additional[0]
        else: additional = {}
        for k in additional: cdata[short_name]['AcquisitionAnalytes-'+k] = additional[k]
     # now we can get all our meta columns
     meta_labels = sorted(functools.reduce(lambda x, y: x.union(y),[set(cdata[k].keys()) for k in cdata.keys()],set()))
     #print(meta_labels)
     if not args.no_header:
        of.write('short_name'+"\t"+"\t".join(meta_labels)+"\n")
     if args.R:
        of.close()
        return
     for name in cdata:
        #ostr =  name+"\t"+"\t".join(
        labs = [name]+[cdata[name][x] if x in cdata[name] else '' for x in meta_labels]
        ostr = "\t".join([x if x is not None else '' for x in labs])+"\n"
        of.write(ostr)
     return

   allparams = [set(fcs.text.parameter_data[x].keys()) for x in fcs.text.parameter_data.keys()]
   basic = functools.reduce(lambda x, y: x.union(y), allparams, set())
   pfields = ['$PnN'] + sorted([x for x in basic if x != '$PnN'])
   if not args.no_header:
      of.write("\t".join(pfields))
      of.write("\n")
   if args.R:
      of.close()
      return
   for num in fcs.text.parameter_data:
      dat = [fcs.text.parameter_data[num][f] if f in fcs.text.parameter_data[num] else '' for f in pfields]
      of.write("\t".join(dat))
      of.write("\n")

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
