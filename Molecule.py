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

#ORCA = os.environ.get('ORCA')

ORCA='/usr/local/bin'

class Atom:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        self.index            = 0
        self.symbol           = 0  # C   - carbon
        self.name             = 0  # CA  - carbon alpha
        self._type            = 0  # C.3 - tertiary carbon 
        self.MULLIKEN_charge  = 0  # partial charge  -> used in force fields
        self.CHELPG_charge    = 0
        self.LOEWDIN_charge   = 0
        self.ORIGINAL_charge  = 0

        pass


class MolecularSystem:
    """ Class doc 
    """
    
    def __init__ (self, ORCA_parameters = None):
        """ Class initialiser """
        self.basename     = 'mysystem'
        self.charge       = 0
        self.multiplicity = 1
        self.atoms        = []
        
        
        
        self.number_of_H   = None
        self.number_of_unk = None
        

        #--------------------------------------------------------------
        #                O R C A    P A R A M E T E R S
        #--------------------------------------------------------------
        if ORCA_parameters == None:
            self.ORCA_parameters = {
                                    'PAL'        : False   ,
                                    'NPAL'       : 1      ,
                                    'PrintBasis' : False  ,
                                    'bases'      : '3-21G', 
                                    'CHELPG'     : True   ,
                                    'method'     : 'HF'   ,
                                    }
        else:
            self.ORCA_parameters = ORCA_parameters
        #--------------------------------------------------------------
        self.bonds = []


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
    
    
    def get_symbol_from_atom_name (self, name = None):
        """ Function doc """
        
        Symbol = name[0]
        
        for char in name[1:]:
            
            try:
                char = int(char)

            except:
                if char == char.capitalize():
                    pass
                else:
                    Symbol += char
            
        return Symbol
    
    
    def Import_MOL2FileToSystem (self, filein, log = True):
        """ Function doc """
        text = open(filein, 'r')
        text = text.readlines()
        #self.chain = Chain()
        total_charge = 0
        
        atoms_initial_index = None
        atoms_final_index   = None
        bonds_final_index   = text.index(text[-1])
        
        
        for line in text:
            
            #line2 = line.split()
            
            if '@<TRIPOS>ATOM' in line:
                atoms_initial_index = text.index(line)
            
            if '@<TRIPOS>BOND' in line:
                atoms_final_index   = text.index(line)
            
            if '@<TRIPOS>SUBSTRUCTURE' in line:
                bonds_final_index   = text.index(line)

        
        
        for index in range(atoms_initial_index, atoms_final_index):
            line2 = text[index].split()

            if len(line2) > 6:
                #rint line2
                atom = Atom()
                atom.index           = line2[0]
                atom.symbol          = self.get_symbol_from_atom_name (name = line2[1])    # C   - carbon
                atom.name            = line2[1]                                            #None  # CA  - carbon alpha
                atom._type           = line2[5]                                            # C.3 - tertiary carbon 
                atom.ORIGINAL_charge = line2[-1]                                           # partial charge  -> used in force fields
                atom.coords          = [float(line2[2]),
                                        float(line2[3]),
                                        float(line2[4])]
                #print atom.ORIGINAL_charge
                self.atoms.append(atom)
                total_charge += float(atom.ORIGINAL_charge)

            
        for index in range(atoms_final_index, bonds_final_index+1):
            #print text[index]
            line  = text[index]
            line2 = line.split()
            try:
                bond = [int(line2[0]),line2[1],line2[2],line2[3]]
                self.bonds.append(bond)
            except:
                pass
            
            
    def export_MOL2File(self                    ,
                        fileout = 'fileout.mol2',
                        resn    = 'UNK'         ,
                        charge  = 'ORIGINAL'    ,
                        ):
        """ Function doc 


        @<TRIPOS>MOLECULE
        *****
         5 4 0 0 0
        SMALL
        GASTEIGER

        @<TRIPOS>ATOM
              1 C          -3.2580    2.0070    0.0000 C.3     1  LIG1       -0.0776
              2 H          -2.1880    2.0070    0.0000 H       1  LIG1        0.0194
              3 H          -3.6147    1.3042    0.7237 H       1  LIG1        0.0194
              4 H          -3.6147    1.7317   -0.9705 H       1  LIG1        0.0194
              5 H          -3.6147    2.9852    0.2468 H       1  LIG1        0.0194
        @<TRIPOS>BOND
             1     1     2    1
             2     1     3    1
             3     1     4    1
             4     1     5    1      
        """
        
         
        
        text =  '@<TRIPOS>MOLECULE\n'
        text += '*****\n'
        text += '%3i %3i 0 0 0 \n'%(len(self.atoms), len(self.bonds))
        text += 'SMALL                                                                       \n'
        text += '%s                                                                    \n' %(charge)
        text += '                                                                            \n'
        text += '@<TRIPOS>ATOM                                                               \n'
        
        for atom in self.atoms:
            
            if charge == 'CHELPG':
                atom_charge = atom.CHELPG_charge
            if charge == 'MULLIKEN':
                atom_charge = atom.MULLIKEN_charge
            if charge == 'LOEWDIN':
                atom_charge = atom.LOEWDIN_charge 
            if charge == 'ORIGINAL':
                atom_charge = atom.ORIGINAL_charge 
            #print atom.coordinates
            text += '%7i %3s       %7.4f %7.4f %7.4f %4s 1  %3s  %8.4f \n' %(int(atom.index), 
                                                                             str(atom.name), 
                                                                             float(atom.coords[0]),
                                                                             float(atom.coords[1]),
                                                                             float(atom.coords[2]),
                                                                             str(atom._type)      , 
                                                                             str(resn[0:3])       ,
                                                                             float(atom_charge))
        
        
        
        
        
        #text += '      1 C          -3.2580    2.0070    0.0000 C.3     1  LIG1       -0.0776'
        #print text
        
        text += '@<TRIPOS>BOND                                                              \n'
        for bond in self.bonds:
            text += '%6s %6s %6s %6s \n' %(bond[0],bond[1],bond[2],bond[3])
        
        
        fileout = open(fileout, 'w')
        fileout.write(text)
        #print text

    def export_ORCA_inputfile (self                , 
                               fileout    = None   ,
                               _type      = 'energy' 
                              ):
        """ Function doc """
        
        
        text  = ''
        text += '# ----------------------------------------------------------------\n'
        text += '#            Orca input file - %s                 \n' %(self.basename)
        text += '# ----------------------------------------------------------------\n'
        
        
        if self.ORCA_parameters['PAL']:
            NPAL = self.ORCA_parameters['NPAL']
        else:
            NPAL = self.ORCA_parameters['NPAL']

        
        if _type == 'energy':
            text += '! '     + self.ORCA_parameters['method'] + '\n'
        
        if _type == 'opt':
            text += '! opt ' + self.ORCA_parameters['method'] + '\n'
        

        
        
        
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
        
        text += '* xyz %3i %3i  \n' %( self.charge , self.multiplicity  )
        
        for atom in self.atoms:
            text += '%s  %4.6f %4.6f %4.6f \n' %(atom.symbol, atom.coords[0], atom.coords[1], atom.coords[2] )
        text += '*                                                                 \n'
        
        fileout = open(fileout, 'w')
        fileout.write(text)
        
    
    def load_XYZ_coordinates_to_system (self, filein):
        """ Function doc 
        
        [0]         [1]                    [2]                   [3]
        C   -3.25795487715671      2.00693616727014      0.00008944956500

        """
        filein =  open(filein , 'r')
        filein =  filein.readlines()
        
        index = 0 
        for line in filein[2:]:
            line = line.replace('\n', '')
            line2 = line.split()
            if len(line2) ==4:
                #print [float(line2[1]),
                #       float(line2[2]),
                #       float(line2[3])]
                       
                #print index , self.atoms[index].coords      
                
                self.atoms[index].coords = [float(line2[1]),
                                                 float(line2[2]),
                                                 float(line2[3])]
            
                #print index, self.atoms[index].coords
                index += 1
            #if len(line2) == 4:
            #    try:
            #        line2[1] == float(line2[1])
                
                

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
                    index  = int(line2[0]) 
                    self.atoms[index].CHELPG_charge = float(line2[3])
                    #print self.atoms[index].name , self.atoms[index].CHELPG_charge
                
        for line in range(MULLIKEN_initial_index, MULLIKEN_final_index):
            line2 = text[line].split()
            if len(line2) == 4:
                try:
                    index  = int(line2[0]) 
                    self.atoms[index].MULLIKEN_charge = float(line2[3])
                    #print self.atoms[index].name , self.atoms[index].MULLIKEN_charge
                except:
                    #pass
                    print index, line2
                    
        for line in range(LOEWDIN_initial_index, LOEWDIN_final_index):
            line2 = text[line].split()
            if len(line2) == 4:
                index  = int(line2[0]) 
                self.atoms[index].LOEWDIN_charge = float(line2[3])
                #print self.atoms[index].name , self.atoms[index].LOEWDIN_charge

    def run_ORCA(self, filein = None, fileout = None, _type = 'energy'):
        """ Function doc """
        #subprocess.call('orca', filein, '>', fileout)
        if not os.path.exists('orca_tmp'):
            os.makedirs('orca_tmp')
        if filein == None:
            filein =  'orca_tmp/' + self.basename+'.inp'
        if fileout == None:
            fileout = 'orca_tmp/' + self.basename+'.out'
        
        self.export_ORCA_inputfile (fileout = filein,
                                    _type   = _type)
        
        os.system(ORCA + '/orca '+filein+ ' > ' + fileout)
        
        self.ParseORCALogFile(fileout)
        if _type == 'opt':
            try:
                self.load_XYZ_coordinates_to_system(fileout[:-3]+'xyz')
            except:
                print fileout[:-3]+'xyz', 'not found or corrupted'











