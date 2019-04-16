===========
treeconvert
===========

``treeconvert`` converts NML files [1]_ to SWC [2]_. This allows you to view
(Py)KNOSSOS skeletal reconstructions in SWC viewers, e.g. Amira.

If the NML file consists of multiple trees, a separate SWC file will get
created for each one.

``treeconvert`` will automatically assign the numeric value of an SWC
*structure identifier* if there is a corresponding *comment* in the NML node.
There exist different conventions on which numeric value to use for an
identifier, so ``treeconvert`` will use those of “CNIC data” described here
[2]_ and `here <https://web.archive.org/web/20170324162931/research.mssm.edu/cnic/swc.html>`_
(archive.org, last retrieved on April 16th, 2019).

.. [1] For more information about NML files, visit https://github.com/scalableminds/nml-spec.
.. [2] http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html


Installation
============

``treeconvert`` only has a single dependency: ``declxml``. For convenience,
``declxml`` is included directly inside ``treeconvert``'s source tree.

The ``setup.py`` installs a ``treeconvert`` binary that you can use from your
``PATH``.

Alternatively, go to `Releases <https://github.com/ariadne-service/treeconvert/releases>`_
to download a self-contained zip file.

To execute the ``.pyz`` file, execute it with python: ``python3 treeconvert.pyz -h``.


Requirements
============

Minimum Python version is 3.7.


Usage
=====

::

	$ python3 cmutil.pyz -h
	usage: treeconvert.pyz [-h] --from {NML,PYKNOSSOS_NML} --to {SWC} [--force]
	                       input_file

	Convert annotation files between various formats.

	positional arguments:
	  input_file            Input file. Output file will be created automatically
	                        with extension `.[--to]'.

	optional arguments:
	  -h, --help            show this help message and exit
	  --from {NML,PYKNOSSOS_NML}
	                        input format
	  --to {SWC}            output format
	  --force               overwrite existing output files.

	If the output format is SWC, and if there are multiple trees in the input
	file, treeconvert will create a file for each tree, and append the filename
	with its index.

There a subtle differences between NML files created from KNOSSOS and those
created from PyKNOSSOS. Because of this, the input format must explicitly be
``nml`` or ``pyknossos_nml``.


License
=======

Other than ``declxml`` (released under MIT License), all of ``treeconvert``’s
files are released under the zlib license (c.f. ``LICENSE``).
