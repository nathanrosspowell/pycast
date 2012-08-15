#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PyCast. Authored by Nathan Ross Powell.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
import re
import json

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Slug creation via http://djangosnippets.org/snippets/29/
def slugify( inStr ):
    removelist = ["a", "an", "as", "at", "before", "but",   \
        "by", "for","from","is", "in", "into", "like", "of",\
        "off", "on", "onto","per","since", "than", "the",   \
        "this", "that", "to", "up", "via","with"]
    for a in removelist:
        aslug = re.sub(r'\b'+a+r'\b','',inStr)
    aslug = re.sub('[^\w\s-]', '', aslug).strip().lower()
    aslug = re.sub('\s+', '-', aslug)
    return aslug

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Read the json file and covert it to a python object.
def fileToJson( path ):
    with open ( path, 'r' ) as file:
        jsonString = file.read()
    return json.loads( jsonString )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test for a specific node.
def xmlFilterName( node, name ):
    return node.nodeType == node.ELEMENT_NODE and node.localName == name

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Node access helper.
def xmlGetNode( node, name ):
    for elem in node.childNodes:
        if xmlFilterName( elem, name ):
            return elem

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Generator for specific nodes.
def xmlGenNodes( node, name ):
    for elem in node.childNodes:
        if xmlFilterName( elem, name ):
            yield elem

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Node helper function.
def xmlGetAttrib( node, name ):
    return node.attributes[ name ].firstChild.wholeText

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test if a file exists/can be read.
def fileExists( filePath ):
    try:
        with open( filePath, 'r' ) as file:
            return True
    except:
        return False
