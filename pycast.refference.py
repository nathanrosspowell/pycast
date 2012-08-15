#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PyCast. Authored by Nathan Ross Powell.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import xml.dom.minidom
import datetime
import time
import os
import urllib
import sys
import re
#-----------------------------------------------------------------------------
# URL slug creation via http://djangosnippets.org/snippets/29/
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

def filterName( node, name ):
    return node.nodeType == node.ELEMENT_NODE and node.localName == name

def getNode( node, name ):
    for elem in node.childNodes:
        if filterName( elem, name ):
            return elem

def genNodes( node, name ):
    for elem in node.childNodes:
        if filterName( elem, name ):
            yield elem

def getAttribute( node, name ):
    return node.attributes[ name ].firstChild.wholeText
  
def itemDict( node ):
    data = {}
    for child in node.childNodes:
        if child.localName and child.firstChild:
            if child.localName == "pubDate":
                    time_format = "%a, %d %b %Y %H:%M:%S "
                    dateText = child.firstChild.wholeText
                    dateText = dateText[ : dateText.rfind("+") ]
                    timeStamp = time.mktime(time.strptime(dateText, time_format))
                    data[ "date" ] = datetime.datetime.fromtimestamp(timeStamp)
            elif child.localName == "title":	
                    data[ "title" ] = child.firstChild.wholeText.strip()
        elif child.localName:
            if child.localName == "enclosure":
                data[ "url" ] = child.attributes[ "url" ].firstChild.wholeText.strip()
    return data
    
def genItems( doc ):
    return ( item
             for rss in doc.childNodes 
             if filterName( rss, "rss" )
             for chan in rss.childNodes
             if filterName( chan, "channel" )
             for item in chan.childNodes
             if filterName( item, "item" ) 
           )

def feedOpener( settings, rss ):
    opener = urllib.FancyURLopener({})
    if not os.path.exists( settings[ "cache" ] ):
        os.mkdir( settings[ "cache" ] )
    name = os.path.join( settings[ "cache" ], slugify( rss ) )
    opener.retrieve( rss, name )
    with open( name, 'r' ) as rssXml:
        return xml.dom.minidom.parse( rssXml )
    return None

def getFileName( data ):    
    dateFormat = data[ "date" ].strftime( data[ "dateFormat" ] )
    title = data[ "title" ].title()
    nameFormat = eval( "(%s)" % ( data[ "nameFormat" ], ) )
    seperator = data[ "seperator" ]
    name =  '%s%s%s' % ( nameFormat[ 0 ], seperator, nameFormat[ 1 ] )
    url = data[ "url" ]
    fileExtension = url[ url.rfind("."):]
    fileName = "%s%s" % ( name, fileExtension )
    fileName = fileName.replace(" %s " % seperator, seperator ).replace( ", ", seperator ).replace( " ", "_")
    return fileName

def gotAllData( data ):
    for key in ( "title", "url", "date" ):
        if not data.has_key( key ):
            return False
    return True

def addExtraData( data, feedDict):
    data[ "nameFormat" ] = feedDict.get( "nameFormat", "( title, dateFormat )" )
    data[ "dateFormat" ] = feedDict.get( "dateFormat", "%Y-%m-%d_%H-%M-%S" )
    data[ "seperator" ] = feedDict.get( "seperator", "-" )
    data[ "space" ] = feedDict.get( "space", "_" )
    data[ "startDate" ] = feedDict.get( "startDate", None )
    data[ "fileName" ] = getFileName( data )
    
def getRssData( settings, feedDict ):
    for itemNode in genItems( feedOpener( settings, feedDict[ "rss" ] ) ):
        data = itemDict( itemNode )
        if gotAllData( data ):
            addExtraData( data, feedDict )
            yield data

def getSettingsAndPriority( xmlFile ):
    doc = xml.dom.minidom.parse( xmlFile )
    settings = { "feeds": {} }
    priority = []
    for child in getNode( doc, "podcast").childNodes:
        if filterName( child, "feeds"):
            for feed in child.childNodes:
                if filterName( feed, "feed"):
                    key = None
                    attributeData = {}
                    for i in xrange( feed.attributes.length ):
                        attributeName = feed.attributes.item( i ).localName
                        if attributeName == "name":
                            key = getAttribute( feed, "name" );
                        else:
                            attributeData[ attributeName ] = getAttribute( feed, attributeName );
                    if key:
                        priority.append( key )
                        settings[ "feeds" ][ key ] = attributeData
                    else:
                        print "ERROR, no 'name' attribute" 
        elif child.nodeType == child.ELEMENT_NODE and child.localName:
            settings[ child.localName ] = getAttribute( child, "value" )
    return settings, priority

def listNewFiles( settings, feedDict ):
    folder = settings[ "folder" ]
    new = []
    for data in getRssData( settings, feedDict ):
        fullFilePath = os.path.join( os.path.join( folder, feedDict[ "folder"] ), data[ "fileName" ] )
        if not os.path.exists( fullFilePath ):
            data[ "fullFilePath" ] = fullFilePath
            new.append( data )
    return new

def newFileStatus( newDict, priority, verbose ):
    files = False
    for key in priority:
        value = newDict.get( key, None)
        if not value:
            continue
        files = True
        print "%d NEW: %s" % ( len( value ), key )
        if verbose:
            for podcast in value:
                print "\t%s" % ( podcast[ "fileName" ], )
    if not files:
        print "All RSS feeds are up to date."
    return files

def download( url, filePath, verbose, dryRun):
    dirName = os.path.os.path.dirname( filePath )
    if not os.path.exists( dirName ):
        os.makedirs( dirName )
    print "\tStarting", url, "as", filePath, "..."
    try:
        if not dryRun:
            urllib.urlretrieve( url, filePath )
        print "\t\tDownloaded!"
    except KeyboardInterrupt:
        if verbose:
            print "\nKeyboardInterrupt, removing: %s\n" % ( filePath, )
        if os.path.exists( filePath ):
            os.remove( filePath )
        raise
    except:
        print "\nERROR : removing %s" % ( filePath, )
        if os.path.exists( filePath ):
            os.remove( filePath )
    
def downloadAll( newDict, priority, verbose, dryRun ):
    for key in priority:
        value = newDict.get( key, None)
        if not value:
            continue
        print "Downloading %s from: %s" %( len( value ), key )
        value.sort( reverse=True, key=lambda v: v[ "date" ] )
        for item in value:
            download( item[ "url" ], item[ "fullFilePath" ], verbose, dryRun )

def main( xmlFile, verbose, dryRun ):
    settings, priority = getSettingsAndPriority( xmlFile )
    print "SETTINGS\n", settings
    print "\npriority\n", priority
    newFiles = {}
    for key, value in settings[ "feeds" ].iteritems():
        new = listNewFiles( settings, value )
        if new != []:
            newFiles[ key ] = new
    if newFileStatus( newFiles, priority, verbose ):
        downloadAll( newFiles, priority, verbose, dryRun )

if __name__ == "__main__":
    if len( sys.argv ) < 2:
        print "Usage: <podcast: xml file> <verbose: 1 or 0: optional> <dryrun: 1 or 0: optional>"
    else:
        podcastXML = sys.argv[ 1 ]
        try:
            verbose = sys.argv[ 2 ]
        except:
            verbose = False
        try:
            dryRun = sys.argv[ 3 ]
        except:
            dryRun = False
        main( podcastXML, verbose, dryRun )
