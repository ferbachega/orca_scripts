#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ORCA.py
#  
#  Copyright 2016 Fernando Bachega <fernando@Fenrir>
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
from pprint import pprint
import subprocess
import os
ORCA='/home/fernando/programs/orca_3_0_3_linux_x86-64'

class Atom:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        self.index  = 0
        self.symbol = None  # C   - carbon
        self.name   = None  # CA  - carbon alpha
        self._type  = None  # C.3 - tertiary carbon 
        self.charge = None  # partial charge  -> used in force fields
        self.coordinates = [0.0, 0.0, 0.0]
        pass

class Residue:
    """ Class initialiser """

    def __init__ (self):
        self.atoms = []
        self.resi  = 0
        self.resn  = None  # C   - carbon
        self.chain = None
        pass

class Chain:
    """ Class initialiser """

    def __init__ (self):
        self.residues = []
        self.name     = 'A'
        pass





class MolecularSystem:
    """ Class doc 
          1 N           7.0960    3.5310    6.6840 N.3     4  GLY4       -0.1210
          1 C          -8.5520    1.2889    0.0129 C.3     1  LIG1       -0.0653
    
    """
    
    def __init__ (self):
        """ Class initialiser """
        self.basename     = 'mysystem'
        self.charge       = 0
        self.multiplicity = 1
        self.atoms = []
        
        
        pass
        
    
    def Import_MOL2FileToSystem (self, filein, log = True):
        """ Function doc """
        text = open(filein, 'r')
        
        #self.chain = Chain()
        total_charge = 0
        
        for line in text:
            line2 = line.split()
            if len(line2) > 6:
                atom = Atom()
                atom.index  = line2[0]
                atom.symbol = None       # C   - carbon
                atom.name   = line2[1]   #None  # CA  - carbon alpha
                atom._type  = line2[5]       # C.3 - tertiary carbon 
                atom.charge = line2[-1]       # partial charge  -> used in force fields
                atom.coords = [float(line2[2]),
                               float(line2[3]),
                               float(line2[4])]
                self.atoms.append(atom)
                total_charge += float(atom.charge)
                
                #print line2
        if log:
            print 'number of atoms:', len(self.atoms)
            print 'total charge   :', total_charge


    def ExportORCAInputFile (self, 
                             fileout    = None   , 
                             _type      = 'HF'   ,
                             base       = '3-21G',
                             PrintBasis = False  ,
                             CHELPG     = True   ,
                            ):
        """ Function doc """
        text  = ''
        text += '# ================================================================\n'
        text += '# Orca input file made in Gabedit                                 \n'
        text += '# ================================================================\n'
        
        text += '! ' + _type + '\n'
        
        if PrintBasis:
            PrintBasis = 'PrintBasis'
        else:
            PrintBasis = ''

        text += '! ' + PrintBasis + ' ' +  base
        
        
        
        if CHELPG:
            text += ' CHELPG \n'
        else:
            text += ' \n'
       
       
        #text += '%output                                                           \n'
        #text += '   tprint[p_mos] 1                                                \n'
        #text += 'end #output                                                       \n'
        
        text += '* xyz 0   1                                                       \n'
        for atom in self.atoms:
            text += '%s  %4.6f %4.6f %4.6f \n' %(atom.name, atom.coords[0], atom.coords[1], atom.coords[2] )
        text += '*                                                                 \n'
        
        fileout = open(fileout, 'w')
        fileout.write(text)
        
        #text += '%geom Constraints                                                 \n'
        #text += '{C 0 C}                                                           \n'
        #text += '{C 1 C}                                                           \n'
        #text += '{C 2 C}                                                           \n'
        #text += '{C 3 C}                                                           \n'
        #text += 'end #Constraints                                                  \n'
        #text += 'invertConstraints true                                            \n'
        #text += 'end #geom                                                         \n'
    
    def ParseORCALogFile (self, filein = None):
        """ Function doc """

        text = open(filein, 'r')
        #self.chain = Chain()
       
        for line in text:
            print line
            line2 = line.split()
    
    
    def RunORCA(self, filein = None, fileout = None):
        """ Function doc """
        #subprocess.call('orca', filein, '>', fileout)
        
        self.ExportORCAInputFile (fileout = filein)
        
        os.system(ORCA + '/orca '+filein+ ' > ' + fileout)
        
        self.ParseORCALogFile(fileout)


mol = MolecularSystem()
mol.Import_MOL2FileToSystem (filein = '/home/fernando/programs/orca_scripts/examples/butane.mol2')
#mol.ExportORCAInputFile    (fileout = '/home/fernando/programs/orca_scripts/examples/butane.inp')
mol.RunORCA(filein  = '/home/fernando/programs/orca_scripts/examples/butane.inp', 
            fileout = '/home/fernando/programs/orca_scripts/examples/butane.out')
