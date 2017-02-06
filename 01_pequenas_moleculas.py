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



molecules = [
            'examples/butane.mol2'     ,
            #'examples/etane.mol2'      ,
            #'examples/etanol.mol2'     ,
            #'examples/metane.mol2'     ,
            #'examples/metylamine.mol2' ,
            ]
'''
molecules = [
            'Mariana/1_12a.mol2',
            'Mariana/2_06a.mol2',
            'Mariana/2_09c.mol2',
            'Mariana/2_20a.mol2',
            'Mariana/2_23d.mol2',
            'Mariana/2_34a.mol2',
            ]
'''





#'''
for molecule in molecules:
    basename = molecule.split('/')
    basename = basename[-1]
    basename = basename[:-5]
    
    print molecule

    #       Aqui eh feito o setup do calculo
    #---------------------------------------------------------------------------
    mol = MolecularSystem()
    mol.basename = basename
    mol.Import_MOL2FileToSystem (filein = molecule, log = False)
    mol.ORCA_parameters['method'] = 'HF'#'B3LYP'
    mol.ORCA_parameters['bases'] =  '3-21G'
    mol.run_ORCA(_type = 'energy')   # opcoes energy ou opt
    
    #mol.multiplicity = 1
    #mol.charge       = 0
    #---------------------------------------------------------------------------
    method = mol.ORCA_parameters['method']
    
    #       EXPORTANTO OS ARQUIVOS MOL2 COM AS CARGAS DESEJADAS
    #---------------------------------------------------------------------------
    mol.export_MOL2File(fileout = molecule[:-4]+method+'_MULLIKEN.mol2', charge ='MULLIKEN')
    mol.export_MOL2File(fileout = molecule[:-4]+method+'_CHELPG.mol2'  , charge ='CHELPG'  )
    mol.export_MOL2File(fileout = molecule[:-4]+method+'_LOEWDIN.mol2' , charge ='LOEWDIN' )
    #---------------------------------------------------------------------------
#'''

for molecule in molecules:
    basename = molecule.split('/')
    basename = basename[-1]
    basename = basename[:-5]
    
    print molecule
    mol = MolecularSystem()
    mol.basename = basename
    mol.Import_MOL2FileToSystem (filein = molecule, log = False)

    mol.ORCA_parameters['method'] = 'HF'#'B3LYP'
    mol.ORCA_parameters['bases'] =  '3-21G'

    mol.run_ORCA(_type = 'opt')
    mol.export_MOL2File(fileout = molecule[:-4]+method+'_MULLIKEN_opt.mol2', charge ='MULLIKEN')
    mol.export_MOL2File(fileout = molecule[:-4]+method+'_CHELPG_opt.mol2'  , charge ='CHELPG'  )
    mol.export_MOL2File(fileout = molecule[:-4]+method+'_LOEWDIN_opt.mol2' , charge ='LOEWDIN' )

