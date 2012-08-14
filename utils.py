#!/usr/bin/python
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
