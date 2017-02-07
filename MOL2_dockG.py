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

method = 'AM1'#'HF'
basis  = ''   #'3-21G'
folder = 'data/MOL2_dockG/'


molecules = [
            folder+'/1_01.mol2' ,
            folder+'/1_05.mol2' ,
            folder+'/1_09.mol2' ,
            folder+'/1_12a.mol2',
            folder+'/1_12b.mol2',
            folder+'/1_14a.mol2',
            folder+'/1_14b.mol2',
            folder+'/2_04a.mol2',
            folder+'/2_04b.mol2',
            folder+'/2_04c.mol2',
            folder+'/2_04d.mol2',
            folder+'/2_04e.mol2',
            folder+'/2_06a.mol2',
            folder+'/2_06b.mol2',
            folder+'/2_06c.mol2',
            folder+'/2_09a.mol2',
            folder+'/2_09b.mol2',
            folder+'/2_09c.mol2',
            folder+'/2_09d.mol2',
            folder+'/2_09e.mol2',
            folder+'/2_14a.mol2',
            folder+'/2_14b.mol2',
            folder+'/2_14c.mol2',
            folder+'/2_18.mol2' ,
            folder+'/2_20a.mol2',
            folder+'/2_20b.mol2',
            folder+'/2_23a.mol2',
            folder+'/2_23b.mol2',
            folder+'/2_23c.mol2',
            folder+'/2_23d.mol2',
            folder+'/2_23e.mol2',
            folder+'/2_23f.mol2',
            folder+'/2_23g.mol2',
            folder+'/2_34a.mol2',
            folder+'/2_34b.mol2',
            folder+'/2_34c.mol2',
            folder+'/2_35a.mol2',
            folder+'/2_35b.mol2',
            folder+'/2_35c.mol2',
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
#'''

for molecule in molecules:
    basename = molecule.split('/')
    basename = basename[-1]
    basename = basename[:-5]
    
    print molecule
    mol = MolecularSystem()
    mol.basename = basename
    mol.Import_MOL2FileToSystem (filein = molecule, log = False)

    mol.ORCA_parameters['method'] = method#'HF'#'B3LYP'
    mol.ORCA_parameters['bases'] =  basis #'3-21G'

    mol.run_ORCA(_type = 'opt')
    mol.export_MOL2File(fileout = molecule[:-4]+label+'_MULLIKEN_opt.mol2', charge ='MULLIKEN')
    mol.export_MOL2File(fileout = molecule[:-4]+label+'_CHELPG_opt.mol2'  , charge ='CHELPG'  )
    mol.export_MOL2File(fileout = molecule[:-4]+label+'_LOEWDIN_opt.mol2' , charge ='LOEWDIN' )

