#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
import xml.dom.minidom
# Local.
import utils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global data
Config = "config.xml"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Settings class. Holds the xml data in python format.
class Settings:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Constructor.
    def __init__( self, configFile ):
        self.configFile = configFile
        self.setFromXml()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data set function.
    def setFromXml( self ):
        self.data = self.getFromXml( self.configFile )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Data get function.
    def getFromXml( self, configFile ):
        # Get the xml document.
        doc = xml.dom.minidom.parse( configFile  )
        # Set up the inital data structure for settings.
        settings = { "feeds": {} }
        # Iterate from the root node.
        for child in utils.xmlGetNode( doc, "podcast" ).childNodes:
            # Only process the feeds node.
            if utils.xmlFilterName( child, "feeds" ):
                for feed in child.childNodes:
                    # Only process the feed nodes
                    if utils.xmlFilterName( feed, "feed" ):
                        print "FEED!"
                        key = None
                        atrib = {}
                        # Build up an attribute dictionary.
                        for i in xrange( feed.attributes.length ):
                            name = feed.attributes.item( i ).localName
                            if name == "name":
                                key = utils.xmlGetAttrib( feed, "name" )
                            else:
                                atrib[ name ] = utils.xmlGetAttrib( feed, name )
                        if key:
                            settings[ "feeds" ][ key ] = atrib
            # Else, try and add a general node with a value setting.
            elif child.nodeType == child.ELEMENT_NODE and child.localName:
                settings[ child.localName ] = utils.xmlGetAttrib( child, "value" )
        return settings

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test run.
if __name__ == "__main__":
    settings = Settings( "config.xml" )
    print settings.data
