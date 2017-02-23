#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  01_pequenas_moleculas.py
#  
#  Copyright 2016 farminf <farminf@farminf-3>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from Molecule import MolecularSystem
from pprint import pprint
import subprocess
import os
import sys

inputs     = sys.argv
method     = 'AM1'#'HF'
basis      = ''   #'3-21G'
if os.getcwd() not in inputs[1]:
	folder 	   = os.getcwd()+'/'+inputs[1]#'data/MOL2_dockG/'
	if folder[-1]!='/':
		folder = folder+'/'
else:
	folder 	   = inputs[1]#'data/MOL2_dockG/'
	if folder[-1]!='/':
		folder = folder+'/'


molecules_raw = os.listdir(folder) #molecules names
molecules     = [folder+x for x in molecules_raw] #molecules full path

#---------------------------------------------------------------------------
#			Dataset information
#---------------------------------------------------------------------------
print 'Working directory: %s ' %folder
print '%s molecules found in the directory' %len(molecules_raw)
if len(inputs)>=3: print "%s format was selected\n\n" %inputs[2]
#---------------------------------------------------------------------------


for molecule in molecules:
	if len(inputs)>=3:
		mol_format = inputs[2]
		if mol_format not in molecule:
			print 'Wrong molecule format for %s' %molecule
			basename = 'Empty'
		else:
			basename = molecule.split('/')[-1].split('.'+mol_format)[0]
	else:		
		print 'No molecule format selected. Things can go wrong if theres \n a point in the name of your molecule'
		basename = molecule.split('/')[-1].split('.')[0]

	print molecule.split('/')[-1]

	#       Aqui eh feito o setup do calculo
	#---------------------------------------------------------------------------
	mol = MolecularSystem()
	mol.basename = basename
	mol.Import_MOL2FileToSystem (filein = molecule, log = False)
	mol.ORCA_parameters['method'] = method#'AM1'#'B3LYP'
	mol.ORCA_parameters['bases'] =  basis #''#'3-21G'
	mol.run_ORCA(_type = 'energy')   # opcoes energy ou opt

	#mol.multiplicity = 1
	#mol.charge       = 0
	#---------------------------------------------------------------------------
	label = mol.ORCA_parameters['method']+'_'+mol.ORCA_parameters['bases']

	#       EXPORTANTO OS ARQUIVOS MOL2 COM AS CARGAS DESEJADAS
	#---------------------------------------------------------------------------
	mol.export_MOL2File(fileout = molecule[:-4]+label+'_MULLIKEN.mol2', charge ='MULLIKEN')
	mol.export_MOL2File(fileout = molecule[:-4]+label+'_CHELPG.mol2'  , charge ='CHELPG'  )
	mol.export_MOL2File(fileout = molecule[:-4]+label+'_LOEWDIN.mol2' , charge ='LOEWDIN' )
	#---------------------------------------------------------------------------


	mol.run_ORCA(_type = 'opt')
	mol.export_MOL2File(fileout = molecule[:-4]+label+'_MULLIKEN_opt.mol2', charge ='MULLIKEN')
	mol.export_MOL2File(fileout = molecule[:-4]+label+'_CHELPG_opt.mol2'  , charge ='CHELPG'  )
	mol.export_MOL2File(fileout = molecule[:-4]+label+'_LOEWDIN_opt.mol2' , charge ='LOEWDIN' )















#print molecules
