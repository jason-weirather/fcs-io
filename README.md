# fcs-io
FCS file handling 

Vist [The manual](../blob/master/fcs-io.pdf)

*Lets slice and dice FCS files like pros.*

Main purpose:
1. A class for working with FCS files in python pipelines
2. A command line interface for working with FCS files

## A class for working with FCS files in python pipelines

With flow cytometry drawing growing interest from data scientists
working with these datasets requires a class to make the FCS file
a more mutable format. This is a pythonic solution with minimal
dependencies beyond core python. 🐍  

**Goals of this package include ⚽ 🥅**

* Read FCS 3.0+ files
* Allow FCS files to be filtered and sliced.
  - Cell index (subsetting)
  - Parameter value (gating)
* Parameter magement
  - remove parameters
  - reorder parameters
* Allow concatonation of datasets
* Output pythonic matrix data for analysis

## A command line interface for working with FCS files

We also want to provide the fcs-io command to work directly with FCS files
from the command line.
