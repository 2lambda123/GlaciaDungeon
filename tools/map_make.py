def gen_h(symbol,w,h):
    """Generates a map source with specified symbol, width, and height.
    Parameters:
        - symbol (str): The symbol to be used in the map source.
        - w (int): The width of the map source.
        - h (int): The height of the map source.
    Returns:
        - MapSource: A map source with the specified symbol, width, and height.
    Processing Logic:
        - Generate map source with given parameters."""
    
    return \
f"""#pragma once
#include "map_source.h"

extern const unsigned char {symbol}_src[];

inline const struct MapSource {symbol} = {{{w},{h}, {symbol}_src}};
"""

def gen_c(symbol,w,h):
    """
    #include "{symbol}.maps.h"
    //const struct MapSource {symbol} = ;"""
    
    return \
f"""
#include "{symbol}.maps.h"

//const struct MapSource {symbol} = ;
"""

class MapSource:
    def __init__(self,w,h,s):
        """"This function initializes an object with given width, height, and source. It assigns the values to corresponding attributes of the object."
        Parameters:
            - w (int): Width of the object.
            - h (int): Height of the object.
            - s (str): Source of the object.
        Returns:
            - None: This function does not return any value.
        Processing Logic:
            - Assigns width, height, and source.
            - No validation or manipulation of values.
            - Used to create objects with specific attributes."""
        
        self.width=w
        self.height=h
        self.src=s
        
    def set_name(self, name):
        """"Sets the name of the object to the given name.
        Parameters:
            - name (str): The name to be set for the object.
        Returns:
            - None: Does not return anything.
        Processing Logic:
            - Sets the name attribute.
            - Uses the self keyword.
            - Only takes in one parameter.""""
        
        self.name=name
        
    def write(self):
        """"Creates and writes two files, a .maps.s and .maps.h file, using the provided name, source, width, and height parameters."
        Parameters:
            - name (str): The name of the files to be created.
            - src (str): The source code to be written into the .maps.s file.
            - width (int): The width of the map to be written into the .maps.h file.
            - height (int): The height of the map to be written into the .maps.h file.
        Returns:
            - None: This function does not return any values.
        Processing Logic:
            - Creates two files with the provided name.
            - Writes the source code into the .maps.s file.
            - Writes the map dimensions into the .maps.h file."""
        
        open(self.name+".maps.s","w").write(gen_s(self.name+"_src", self.src))
        open(self.name+".maps.h","w").write(gen_h(self.name, self.width, self.height))        
        
        

import struct

def read_map(file):
    """Reads a map file and returns a MapSource object.
    Parameters:
        - file (str): The path to the map file.
    Returns:
        - MapSource: An object containing the map width, height, and source data.
    Processing Logic:
        - Opens the file in binary mode.
        - Unpacks the first 4 bytes as an integer and assigns it to w.
        - Unpacks the next 4 bytes as an integer and assigns it to h.
        - Reads the remaining data and assigns it to src.
        - Prints the type of src.
        - Returns a MapSource object with the width, height, and source data."""
    
    with open(file, "rb") as f:
        w = struct.unpack('i', f.read(4))[0]
        h = struct.unpack('i', f.read(4))[0]
        src = f.read()
    print(type(src))
    return MapSource(w,h,src) 

#def gen_c(symbol, 

def gen_s(symbol, data):    
    """Generates a string of data in hexadecimal format to be used in an assembly file.
    Parameters:
        - symbol (str): The name of the symbol to be used in the assembly file.
        - data (bytes): The data to be converted to hexadecimal format.
    Returns:
        - str: A string of data in hexadecimal format to be used in an assembly file.
    Processing Logic:
        - Converts the data to a bytearray.
        - Adds a 0 byte if the length of the data is odd.
        - Converts the data to hexadecimal format.
        - Splits the data into groups of 2 characters.
        - Reverses the order of the characters in each group.
        - Adds "0x" to the beginning of each group.
        - Joins the groups of data into a string.
        - Splits the string into groups of 8 lines.
        - Joins the groups of lines into a string.
        - Returns the string of data in hexadecimal format."""
    
    str_dat=".word "
    data = bytearray(data)
    if(len(data)%2==1):
        data.append(0)
    data=data.hex()
    data = [data[i:i+2] for i in range(0,len(data),2)]
    data = ["0x"+"".join(data[i:i+2][::-1]) for i in range(0,len(data),2)]
    data = "\n".join(["\t.hword "+", ".join(data[i:i+8]) for i in range(0,len(data),8)])
    #print(data)    
    return \
f"""
    .section .rodata
	.align	4
	.global {symbol}
	.hidden {symbol}
{symbol}:
{data}
"""


import sys
import re
import os

curdir = sys.argv[1]
symbol_name = sys.argv[2]

print(curdir, symbol_name)

maps_file = os.path.dirname(curdir)+"/maps/"+symbol_name+".maps"
print(maps_file)

mapsrc = read_map(maps_file)
mapsrc.set_name(symbol_name)

mapsrc.write()
print(mapsrc.width)
print(mapsrc.height)


#open(symbol_name+".maps.s","w").write(gen_s(symbol_name, open(font_file,"rb").read()))
#open(symbol_name+".maps.h","w").write(gen_h(symbol_name))


#open(fname,"w").write(f"""
#pragma once
#include "Astralbrew/text/font.hpp"

#extern const Astralbrew::Text::ReadOnlyFont {name};
#""")

#sname = name+".s"
#oname = name+".astralfont.o"

#open(sname,"w").write(".section text")
