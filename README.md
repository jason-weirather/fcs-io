# fcs-io
FCS file handling

*Lets slice and dice FCS files like pros.*

With flow cytometry drawing growing interest from data scientists
working with these datasets requires a class to make the FCS file
a more mutable format. This class will provide a way to not only
access the data in the FCS file, but to modify fields in it, slice
the file, and write out a new FCS file.

The main purpose of this is to enable working with CYTOF data, and
while it will be nice if we can support all FCS formats written to
standard, the inital goal will be a reliable tool for working with
CYTOF data.

