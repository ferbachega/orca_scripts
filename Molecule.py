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
        self.index           = 0
        self.symbol          = 0  # C   - carbon
        self.name            = 0  # CA  - carbon alpha
        self._type           = 0  # C.3 - tertiary carbon 
        self.MULLIKEN_charge = 0  # partial charge  -> used in force fields
        self.CHELPG_charge   = 0
        self.LOEWDIN_charge  = 0
        self.coordinates     = [0.0, 0.0, 0.0]
        pass


        '''
        print MULLIKEN_final_index, line


        if 'LOEWDIN ATOMIC CHARGES' in line:

        '''

'''
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

'''



class MolecularSystem:
    """ Class doc 
          1 N           7.0960    3.5310    6.6840 N.3     4  GLY4       -0.1210
          1 C          -8.5520    1.2889    0.0129 C.3     1  LIG1       -0.0653
    
    """
    
    def __init__ (self, ORCA_parameters = None):
        """ Class initialiser """
        self.basename     = 'mysystem'
        self.charge       = 0
        self.multiplicity = 1
        self.atoms        = []


        #--------------------------------------------------------------
        #                O R C A    P A R A M E T E R S
        #--------------------------------------------------------------
        if ORCA_parameters == None:
            self.ORCA_parameters = {
                                    'PAL'        : True   ,
                                    'NPAL'       : 1      ,
                                    'PrintBasis' : False  ,
                                    'bases'      : '3-21G', 
                                    'CHELPG'     : True   ,
                                    'method'     : 'HF'   ,
                                    }
        else:
            self.ORCA_parameters = ORCA_parameters
        #--------------------------------------------------------------



    
    def print_status (self, partial_charges = False):
        """ Function doc """
        print '\n\n\n'

        print '--------------------------------------------------------------------------------'
        print '                   Summary for System %10s                   '%(self.basename)
        print '--------------------------------------------------------------------------------'
        print '                                                                                '
        print '---------------------------- Atom Container Summary ----------------------------'
        print 'Number of Atoms        =          %3s  Number of Heavy Atoms  =          %3s'%(len(self.atoms),len(self.atoms))
        print 'Number of Hydrogens    =          %3s  Number of Unknowns     =          %3s'%(len(self.atoms),len(self.atoms))
        print '--------------------------------------------------------------------------------'
        print '                                                                                '
        
        
        #print '----------------------------- Connectivity Summary -----------------------------'
        #print 'Atoms                  =              6                                         '
        #print '--------------------------------------------------------------------------------'
        #print '                                                                                '
        
        
        print '------------------------------- Electronic State -------------------------------'
        print 'Charge                 =          %3i  Multiplicity           =          %3i'%(self.charge,self.multiplicity)
        print '--------------------------------------------------------------------------------'
        print '                                                                                '
   
   
        if partial_charges:
            print '--------------------------------------------------------------------------------'
            print 'INDEX         NAME        MULLIKEN             CHELPG               LOEWDIN   '
            print '--------------------------------------------------------------------------------'
            for atom in self.atoms:
                print '%4s        %4s        %12.8f         %12.8f         %12.8f   ' %(atom.index, 
                                                                                       atom.name , 
                                                                                       atom.MULLIKEN_charge, 
                                                                                       atom.CHELPG_charge, 
                                                                                       atom.LOEWDIN_charge)



   
    
    def setup_orca_calculations (self, method = 'HF'):
        """ Function doc """
        
    
    
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
            self.print_status()
            #print 'number of atoms:', len(self.atoms)
            #print 'total charge   :', total_charge


    def export_ORCA_inputfile (self                , 
                               fileout    = None   , 
                              ):
        """ Function doc """
        
        
        text  = ''
        text += '# ----------------------------------------------------------------\n'
        text += '#            Orca input file - %s                 \n' %(self.basename)
        text += '# ----------------------------------------------------------------\n'
        
        
        
        text += '! ' + self.ORCA_parameters['method'] + '\n'
        
        
        
        
        
        if self.ORCA_parameters['PrintBasis']:
            PrintBasis = 'PrintBasis'
        else:
            PrintBasis = ''
        text += '! ' + PrintBasis + ' ' +  self.ORCA_parameters['bases'] 
        
        
        
        if self.ORCA_parameters['CHELPG']:
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
        

    
    def ParseORCALogFile (self, filein = None):
        """ Function doc """

        text = open(filein, 'r')
        text = text.readlines()
        #self.chain = Chain()
        Print = False
        CHELPG = False
        for line in text:
            #print line
            
            line2 = line.split()
            if 'MULLIKEN ATOMIC CHARGES' in line:
                MULLIKEN_initial_index = text.index(line)
                #Print = True
                #print MULLIKEN_initial_index, line
            if 'Sum of atomic charges' in line:
                #Print = False
                MULLIKEN_final_index = text.index(line)
                #print MULLIKEN_final_index, line


            if 'LOEWDIN ATOMIC CHARGES' in line:
                LOEWDIN_initial_index = text.index(line)
                #Print = True
                #print LOEWDIN_initial_index, line
            if 'LOEWDIN REDUCED ORBITAL CHARGES' in line:
                #Print = False
                LOEWDIN_final_index = text.index(line)
                #print LOEWDIN_final_index, line



            if 'CHELPG Charges' in line:
                CHELPG_initial_index = text.index(line)
                CHELPG =True
                #Print = True
                #print CHELPG_initial_index, line
            if 'Total charge:' in line:
                #Print = False
                CHELPG_final_index = text.index(line)
                #print CHELPG_final_index, line
            
        if CHELPG:        
            for line in range(CHELPG_initial_index, CHELPG_final_index):
                line2 = text[line].split()
                if len(line2) == 4:
                    index  = int(line2[0]) -1
                    self.atoms[index].CHELPG_charge = float(line2[3])
                    #print self.atoms[index].name , self.atoms[index].CHELPG_charge
                
        for line in range(MULLIKEN_initial_index, MULLIKEN_final_index):
            line2 = text[line].split()
            if len(line2) == 4:
                index  = int(line2[0]) -1
                self.atoms[index].MULLIKEN_charge = float(line2[3])
                #print self.atoms[index].name , self.atoms[index].MULLIKEN_charge
                
        for line in range(LOEWDIN_initial_index, LOEWDIN_final_index):
            line2 = text[line].split()
            if len(line2) == 4:
                index  = int(line2[0]) -1
                self.atoms[index].LOEWDIN_charge = float(line2[3])
                #print self.atoms[index].name , self.atoms[index].LOEWDIN_charge


    def run_ORCA(self, filein = None, fileout = None):
        """ Function doc """
        #subprocess.call('orca', filein, '>', fileout)
        
        
        if filein == None:
            filein = self.basename+'.inp'
        if fileout == None:
            fileout = self.basename+'.out'
        
        self.export_ORCA_inputfile (fileout = filein)
        
        os.system(ORCA + '/orca '+filein+ ' > ' + fileout)
        
        self.ParseORCALogFile(fileout)


    '''
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
        text += '# Orca input file made in ORCA SCRIPT                             \n'
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
        #text += 'end #geom    
        '''

molecules = [
            '/home/fernando/programs/orca_scripts/examples/butane.mol2'     ,
            '/home/fernando/programs/orca_scripts/examples/etane.mol2'      ,
            '/home/fernando/programs/orca_scripts/examples/etanol.mol2'     ,
            '/home/fernando/programs/orca_scripts/examples/metane.mol2'     ,
            '/home/fernando/programs/orca_scripts/examples/metylamine.mol2' ,
            ]

# simple test
'''
mol = MolecularSystem()
mol.Import_MOL2FileToSystem (filein = '/home/fernando/programs/orca_scripts/examples/butane.mol2', log = False)
mol.run_ORCA()
mol.print_status(partial_charges = True)
'''

for molecule in molecules:
    basename = molecule.split('/')
    basename = basename[-1]
    basename = basename[:-5]
    
    mol = MolecularSystem()
    mol.basename = basename
    mol.Import_MOL2FileToSystem (filein = molecule, log = False)
    mol.run_ORCA()
    mol.print_status(partial_charges = True)














