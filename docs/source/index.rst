.. fcs-io documentation master file, created by
   sphinx-quickstart on Sat Jun  3 13:37:30 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to fcs-io's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Command line interface
======================

`fcs-io`
++++++++

**Access sub-commands for working with FCS files**

This command will always need to be followed by an operation command.
If the operation is missing, a list of available options
will be provided.

.. code-block:: bash

   $ fcs-io -h

.. program-output:: fcs-io -h

.. automodule:: fcsio.cli

`cat`
-----
**Concatonate events of FCS files**

.. code-block:: bash

   $ fcs-io cat -h

.. program-output:: fcs-io cat -h

.. automodule:: fcsio.cli.utilities.cat

`describe`
----------
**Summary of FCS file contents**

.. code-block:: bash

   $ fcs-io describe -h

.. program-output:: fcs-io describe -h

.. automodule:: fcsio.cli.utilities.describe

`enumerate`
-----------
**Add an enumeration channel to the paremeters**

.. code-block:: bash

   $ fcs-io enumerate -h

.. program-output:: fcs-io enumerate -h

.. automodule:: fcsio.cli.utilities.enumerate

`filter`
--------
**Remove events based on filtering criteria**

.. code-block:: bash

   $ fcs-io filter -h

.. program-output:: fcs-io filter -h

.. automodule:: fcsio.cli.utilities.filter

`other`
--------
**Extract OTHER user defined fields**

.. code-block:: bash

   $ fcs-io other -h

.. program-output:: fcs-io other -h

.. automodule:: fcsio.cli.utilities.other

`parameters`
------------
**Write a table of parameter information**

.. code-block:: bash

   $ fcs-io parameters -h

.. program-output:: fcs-io parameters -h

.. automodule:: fcsio.cli.utilities.parameters

`reorder`
---------
**Reorder parameters**

.. code-block:: bash

   $ fcs-io reorder -h

.. program-output:: fcs-io reorder -h

.. automodule:: fcsio.cli.utilities.reorder

`rm`
--------
**Remove parameters**

.. code-block:: bash

   $ fcs-io rm -h

.. program-output:: fcs-io rm -h

.. automodule:: fcsio.cli.utilities.rm

`simulate`
----------
**Create a new FCS file from nothing with simulated data**

.. code-block:: bash

   $ fcs-io simulate -h

.. program-output:: fcs-io simulate -h

.. automodule:: fcsio.cli.utilities.simulate

`strip`
-------
**Trim keywords and data segments from a file (but not whole parameters)**

.. code-block:: bash

   $ fcs-io strip -h

.. program-output:: fcs-io strip -h

.. automodule:: fcsio.cli.utilities.strip

`tsv2fcs`
---------
**Convert a TSV file of parameter columns and event rows to an FCS**

.. code-block:: bash

   $ fcs-io tsv2fcs -h

.. program-output:: fcs-io tsv2fcs -h

.. automodule:: fcsio.cli.utilities.tsv2fcs

`view`
------
**View the data from an fcs file**

.. code-block:: bash

   $ fcs-io view -h

.. program-output:: fcs-io view -h

.. automodule:: fcsio.cli.utilities.view

Modules
=======

FCS
+++
.. automodule:: fcsio
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
.. automodule:: fcsio.filter
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

HEADER
++++++
.. automodule:: fcsio.header
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

TEXT segment
++++++++++++
.. automodule:: fcsio.text
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
.. automodule:: fcsio.text.standard
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
.. automodule:: fcsio.text.parameters
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

DATA segment
++++++++++++
.. automodule:: fcsio.data
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

simulate data
+++++++++++++
.. automodule:: fcsio.simulate
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
