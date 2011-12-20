# abitbx #

abitbx is a wrapper of utility functions that can be used on top of cctbx 

cctbx http://cctbx.sourceforge.net/

### Dependencies ###

- cctbx v.X.X.X
- python 2.7
- numpy
- pyyaml
- jsonschema (https://bitbucket.org/IanLewis/jsonschema/)



### Installing cctbx ###

You can either install the cctbx bundle with it's own version of python, or compile cctbx to use your own version of python. Since many people are going to be using other libraries (e.g., pymongo), it's better to compile cctbx against your existing python install. This will allow you to still use easy_install, or pip.

	$> wget http://cci.lbl.gov/cctbx_build/results/last_published/cctbx_bundle.tar.gz


	$> mkdir cctbx-1-19-2011
	$> cd cctbx-1-19-2011

	$> gunzip -c cctbx_bundle.tar.gz | tar xf -

	$> mkdir cctbx_build
	$> cd cctbx_build

	$> python2.7 ../cctbx_sources/libtbx/configure.py mmtbx
	#or use the abspath to avoid potential confusion
	$> /opt/local/bin/bin/python2.7 ../cctbx_sources/libtbx/configure.py mmtbx
	

	# where 4 is the number of processors
	$> ../bin/libtbx.scons -j 4

	# either add this to your bashrc file

	# or alias 'cctbx' as

	alias cctbx=$HOME/development/cctbx-1-19-2011/cctbx_build/bin/libtbx.python

	# if you have ipython installed
	alias icctbx=$HOME/development/cctbx-1-19-2011/cctbx_build/bin/libtbx.ipython

	#now see if it works
	$> cctbx

	# a python shell should load get fired up
	# load cctbx 
	>>> from cctbx import sgtbx
	# see if existing libraries works (e.g., pymongo, pyyaml, ....)
	>>> import pymongo
	>>> import yaml
	# if abitbx is in your PYTHONPATH
	>>> import abitbx
	>>> print abitbx.version()
	

### Using abitbx ###

A few examples should go here

#### Using the Library ####
- What is an xdict?
- What is an sdict?

#### Using the commandline tools ####
- cif2converter.py
- cif2xrd.py
- analyze_cif.py


### F.A.Q. ###
- Why use cctbx ?
