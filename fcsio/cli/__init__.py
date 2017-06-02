"""This is the front end fof the command line utility.  Features can
be accessed according to the available commands"""

import sys, argparse, pkgutil
from importlib import import_module
import os.path
import fcsio.cli.utilities

def main():
   """save the full command"""
   cache_argv = sys.argv
   front_end_args = sys.argv[:2]
   back_end_args = sys.argv[1:]
   """only parse the front end args"""
   sys.argv = front_end_args
   args = do_args()
   sys.argv = cache_argv # put the full arguments back

   """Now import modules accordingly"""
   task_module = import_module('fcsio.cli.utilities.'+args.task)
   """Launch the module with its commands"""
   task_module.external_cmd(" ".join(back_end_args))

def do_args():
   """get the list of possible utilities"""
   util_path = os.path.dirname(fcsio.cli.utilities.__file__)
   """get the package list"""
   packlist = [name for _, name, _ in pkgutil.iter_modules([util_path])]
   parser = argparse.ArgumentParser(description="Work with FCS files from the command line",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   parser.add_argument('task',choices=packlist,help="Specify which task to execute")
   args = parser.parse_args()
   return args
if __name__=="__main__":
   main()
