#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
import xml.dom.minidom

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
        doc = xml.dom.minidom.parse(configFile  )
        # Set up the inital data structure for settings.
        settings = { "feeds": {} }
        # Iterate from the root node.
        for child in self.getNode( doc, "podcast" ).childNodes:
            # Only process the feeds node.
            if self.filterName( child, "feeds" ):
                for feed in child.childNodes:
                    # Only process the feed nodes
                    if self.filterName( feed, "feed" ):
                        print "FEED!"
                        key = None
                        atrib = {}
                        # Build up an attribute dictionary.
                        for i in xrange( feed.attributes.length ):
                            name = feed.attributes.item( i ).localName
                            if name == "name":
                                key = self.getAttribute( feed, "name" )
                            else:
                                atrib[ name ] = self.getAttribute( feed, name )
                        if key:
                            settings[ "feeds" ][ key ] = atrib
            # Else, try and add a general node with a value setting.
            elif child.nodeType == child.ELEMENT_NODE and child.localName:
                settings[ child.localName ] = self.getAttribute( child, "value" )
        return settings

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Test for a specific node.
    def filterName( self, node, name ):
        return node.nodeType == node.ELEMENT_NODE and node.localName == name

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Node access helper.
    def getNode( self, node, name ):
        for elem in node.childNodes:
            if self.filterName( elem, name ):
                return elem

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Generator for specific nodes.
    def genNodes( self, node, name ):
        for elem in node.childNodes:
            if self.filterName( elem, name ):
                yield elem

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Node helper function.
    def getAttribute( self, node, name ):
        return node.attributes[ name ].firstChild.wholeText
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test run.
if __name__ == "__main__":
    settings = Settings( "config.xml" )
    print settings.data
