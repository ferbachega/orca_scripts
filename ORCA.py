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

class Atom:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        self.index  = 0
        self.symbol = None  # C   - carbon
        self.name   = None  # CA  - carbon alpha
        self._type  = None  # C.3 - tertiary carbon 
        self.charge = None  # partial charge  -> used in force fields
        coordinates = [0.0, 0.0, 0.0]
        pass

class Residue:
    """ Class initialiser """

    def __init__ (self):
        self.resi  = 0
        self.resn  = None  # C   - carbon
        self.chain = None
        pass


class Chain:
    """ Class initialiser """

    def __init__ (self):
        self.name  = 'A'
        pass





class MolecularSystem:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        
        self.charge       = 0
        self.multiplicity = 1
        
        
        
        
        pass
        
        
        
        



def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
