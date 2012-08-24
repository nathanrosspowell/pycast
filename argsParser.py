#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PyCast. Authored by Nathan Ross Powell.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
import argparse
# Local.

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Argument parser class.
class ArgsParser:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Take the argv list from the command line. 
    def __init__( self, argList ):
        self.parser = argparse.ArgumentParser( description='PyCast')
        self.parser.add_argument(
            '-u',
            "--update",
            action = "store_true", 
            default = False,
            help = "Update the feeds by gettng the latest from the interent"
        )
        self.parser.add_argument(
            '-n',
            "--name",
            action = "store",
            help = "The name of the feed to look at",
        )
        self.parser.add_argument(
            '-s',
            "--string_item",
            dest = 'itemString',
            nargs = '*',
            default = [],
            help = "One of a list of items to get, by name",
        )
        self.parser.add_argument(
            '-i',
            "--index_item",
            dest = 'itemIndex',
            nargs = '*',
            default = [],
            type = int,
            help = "One of a list of items to get, by index",
        )
        self.setArgs( argList )
        self.generateData()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 
    def setArgs( self, argList ):
        self.argList = argList
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 
    def generateData( self ):
        print "--------------------------------------"
        print self.argList
        print "--------------------------------------"
        self.data = self.parser.parse_args( self.argList ) 

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 
    def getData( self ):
        return self.data

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main execution loop below.
if __name__ == "__main__":
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Imports needed for test.
    import sys
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Run test on ArgsParser.
    parser = ArgsParser( sys.argv[ 1: ] )
    print parser.getData()
