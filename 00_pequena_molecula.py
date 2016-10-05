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
import os






molecule = 'examples/butane.mol2'



basename = molecule.split('/')
basename = basename[-1]
basename = basename[:-5]

#---------------------------------------------------------------------------
#                 Aqui eh feito o setup do calculo
#---------------------------------------------------------------------------
mol = MolecularSystem()
mol.basename = basename
mol.Import_MOL2FileToSystem (filein = molecule, log = False)
mol.ORCA_parameters['method'] = 'B3LYP'               # AM1 PM3 HF B3LYP
mol.ORCA_parameters['bases'] =  '6-31G'               # 3-21G 6-31G 6-31+G*
mol.run_ORCA(_type = 'energy')                        # opcoes energy ou opt
#mol.multiplicity = 1
#mol.charge       = 0
#---------------------------------------------------------------------------




#---------------------------------------------------------------------------
method = mol.ORCA_parameters['method']
#       EXPORTANTO OS ARQUIVOS MOL2 COM AS CARGAS DESEJADAS
#---------------------------------------------------------------------------
mol.Export_MOL2File(fileout = molecule[:-4]+'00_'+method+'_MULLIKEN.mol2', charge ='MULLIKEN')
mol.Export_MOL2File(fileout = molecule[:-4]+'00_'+method+'_CHELPG.mol2'  , charge ='CHELPG'  )
mol.Export_MOL2File(fileout = molecule[:-4]+'00_'+method+'_LOEWDIN.mol2' , charge ='LOEWDIN' )
#---------------------------------------------------------------------------














