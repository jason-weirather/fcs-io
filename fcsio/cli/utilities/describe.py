""" Provide a description of the FCS file and its contents """

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
      if args.output[-3:] == '.gz': of = gzip.open(args.output,'wb')
      else: of = open(args.output,'wb')
   inf.close() # read the bytes and close inputs

   describe_header(fcs,of)
   of.write("\n")
   describe_text(fcs,of)
   of.write("\n")
   describe_data(fcs,of)

def describe_data(fcs,of):
   mat = fcs.data.matrix
   of.write("*** FCS DATA Information ***\n")
   of.write("Events: "+str(len(mat))+"\n")

def describe_text(fcs,of):
   of.write("*** FCS TEXT Information ***\n")
   keys = sorted(fcs.text.keys())
   """Do standard non-parameter keywords first"""
   standard = [x for x in keys if re.match('\$',x)]
   of.write(str(len(standard))+" standard non-parameter keywords\n")
   for k in standard:
      of.write("   "+k+" \t"+fcs.text[k]+"\n")
   """Do nonstandard keywords"""
   nonstandard = [x for x in keys if not re.match('\$',x)]
   if len(nonstandard) == 0:
      of.write("0 non-standard keywords\n")
   else:
      of.write(str(len(standard))+" non-standard keywords\n")
      for k in nonstandard:
         of.write("   "+k+" \t"+fcs.text[k]+"\n")
   """Do parameters"""
   names = [x.short_name for x in fcs.parameters]
   of.write(str(len(names))+" parameters ordered as they appear in the file\n")
   i = 0
   for parameter in fcs.parameters:
      i += 1
      of.write("   "+str(i)+". "+parameter.short_name+" ("+str(len(parameter.get_keywords()))+" keywords)\n")
      for k in sorted(parameter.get_keywords()):
         of.write("      "+k+" \t"+parameter[k]+"\n")

def describe_header(fcs,of):
   """Now the FCS file is loaded up and we can make a nice output"""
   of.write("*** FCS Header Information ***\n")
   of.write("Version: "+fcs.version+"\n")
   text_string = str(len(fcs.text.bytes))+' bytes'
   of.write("TEXT: "+text_string+"\n")
   data_string = str(fcs.standard.ENDDATA-fcs.standard.BEGINDATA+1)+' bytes'
   of.write("DATA: "+data_string+"\n")
   analysis_string = 'False'
   if fcs.standard.BEGINANALYSIS != 0:
      analysis_string = 'True, '
      analysis_string +=str(fcs.standard.ENDANLYSIS-fcs.standard.BEGINANALYSIS+1)+' bytes'
   of.write("ANALYSIS: "+analysis_string+"\n")
   other_string = 'False'
   if len(fcs.other) > 0:
      other_string = 'True, '
      word = 'segment'
      if len(fcs.other) > 1: word = 'segments'
      other_string += str(len(fcs.other))+' '+word+', '
      other_string += str(sum([len(x) for x in fcs.other]))+' bytes'
   of.write('OTHER: '+other_string+"\n")

def do_inputs():
   parser = argparse.ArgumentParser(
            description = "Provide a description of the FCS file and its contents ",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('input',help="Input FCS file or '-' for STDIN '.gz' files will be automatically processed by gzip")
   parser.add_argument('-o','--output',help="Output FCS file or STDOUT if not set")
   args = parser.parse_args()
   return args

def external_cmd(cmd):
   """function for calling program by command through a function"""
   cache_argv = sys.argv
   sys.argv = cmd.split()
   args = do_inputs()
   main(args)
   sys.argv = cache_argv
