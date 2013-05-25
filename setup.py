#!/usr/bin/env python
#
# Setup script for UniConvertor 2.x
#
# Copyright (C) 2013 Igor E. Novikov
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
#

"""
Usage: 
--------------------------------------------------------------------------
 to build package:   python setup.py build
 to install package:   python setup.py install
--------------------------------------------------------------------------
 to create source distribution:   python setup.py sdist
--------------------------------------------------------------------------
 to create binary RPM distribution:  python setup.py bdist_rpm
--------------------------------------------------------------------------
 to create binary DEB distribution:  python setup.py bdist_deb
--------------------------------------------------------------------------

help on available distribution formats: python setup.py bdist --help-formats
"""

import os, sys

import libutils
from libutils import make_source_list, DEB_Builder

#Flags
DEB_PACKAGE = False

############################################################
#
# Package description
#
############################################################
NAME = 'printdesign'
VERSION = '1.0'
DESCRIPTION = 'Universal vector graphics translator'
AUTHOR = 'Igor E. Novikov'
AUTHOR_EMAIL = 'igor.e.novikov@gmail.com'
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
LICENSE = 'GPL v3'
URL = 'http://sk1project.org'
DOWNLOAD_URL = 'http://sk1project.org'
CLASSIFIERS = [
'Development Status :: 5 - Stable',
'Environment :: Desktop',
'Intended Audience :: End Users/Desktop',
'License :: OSI Approved :: LGPL v2',
'License :: OSI Approved :: GPL v3',
'Operating System :: POSIX',
'Operating System :: MacOS :: MacOS X',
'Programming Language :: Python',
"Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
]
LONG_DESCRIPTION = '''
PrintDesign is an open source vector graphics editor similar to CorelDRAW, 
Adobe Illustrator, or Freehand. PrintDesign is oriented for prepress industry, 
so it works with CMYK colorspace and produces CMYK-based PDF and PS output. 

sK1 Project (http://sk1project.org),
Copyright (C) 2010-2013 by Igor E. Novikov
'''
LONG_DEB_DESCRIPTION = ''' .
 PrintDesign is an open source vector graphics editor similar to CorelDRAW,
 Adobe Illustrator, or Freehand. PrintDesign is oriented for prepress industry,
 so it works with CMYK colorspace and produces CMYK-based PDF and PS output.
 . 
 sK1 Project (http://sk1project.org),
 Copyright (C) 2010-2013 by Igor E. Novikov 
 .
'''

############################################################
#
# Build data
#
############################################################
src_path = 'src'
scripts = ['src/printdesign', ]
data_files = []
deb_depends = 'python (>=2.4), python (<<3.0), python-gtk2, python-gnome2, '
deb_depends += 'gnome-desktop-data, python-uniconvertor (>=2.0)'

############################################################
#
# Main build procedure
#
############################################################

if len(sys.argv) == 1:
	print 'Please specify build options!'
	print __doc__
	sys.exit(0)

if len(sys.argv) > 1 and sys.argv[1] == 'bdist_deb':
	DEB_PACKAGE = True
	sys.argv[1] = 'build'

from distutils.core import setup, Extension

setup(name=NAME,
	version=VERSION,
	description=DESCRIPTION,
	author=AUTHOR,
	author_email=AUTHOR_EMAIL,
	maintainer=MAINTAINER,
	maintainer_email=MAINTAINER_EMAIL,
	license=LICENSE,
	url=URL,
	download_url=DOWNLOAD_URL,
	long_description=LONG_DESCRIPTION,
	classifiers=CLASSIFIERS,
	packages=libutils.get_source_structure(),
	package_dir=libutils.get_package_dirs(),
	data_files=data_files,
	scripts=scripts)

#################################################
# .py source compiling
#################################################
libutils.compile_sources()

#################################################
# Implementation of bdist_deb command
#################################################
if DEB_PACKAGE:
	bld = DEB_Builder(name=NAME,
					version=VERSION,
					maintainer='%s <%s>' % (AUTHOR, AUTHOR_EMAIL),
					depends=deb_depends,
					homepage=URL,
					description=DESCRIPTION,
					long_description=LONG_DEB_DESCRIPTION,
					pkg_dirs=libutils.get_package_dirs().keys(),
					scripts=scripts,
					data_files=data_files)
	bld.build()

libutils.clear_build()
