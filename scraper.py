#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
from datetime import datetime
import time
# Local.
import utils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Turn the xml file into usable data.
class Scraper:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__( self, setting, xmls ):
        self.xmls = xmls
        self.items = {}
        self.data = {}
        for name, xml in self.xmls.iteritems():
            self.items[ name ] = []
            feedDict = setting.data[ "feeds" ][ name ]
            feedData = self.addExtraData( feedDict )
            self.data[ name ] = feedData
            for data in self.feedSanitise( feedData, xml, feedDict ):
                self.items[ name ].append( data )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Turn the xml into an easy to use python object.
    def feedSanitise( self, feedData, xml, feedDict ):
        for itemNode in self.genItems( xml ):
            data = self.itemDict( itemNode )
            if self.gotAllData( feedData, data ):
                yield data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Create the python dict for the podcast item
    def itemDict( self, node ):
        data = {}
        for child in node.childNodes:
            if child.localName and child.firstChild:
                if child.localName == "pubDate":
                    timeFormat = "%a, %d %b %Y %H:%M:%S "
                    dateText = child.firstChild.wholeText
                    dateText = dateText[ : dateText.rfind( "+" ) ]
                    timeStrp = time.strptime( dateText, timeFormat )
                    timeStamp = time.mktime( timeStrp )
                    data[ "date" ] = datetime.fromtimestamp( timeStamp )
                elif child.localName == "title":
                    data[ "title" ] = child.firstChild.wholeText.strip()
            elif child.localName:
                if child.localName == "enclosure":
                    urlChild = child.attributes[ "url" ].firstChild
                    data[ "url" ] = urlChild.wholeText.strip()
        return data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #  Check the esential data is there.
    def gotAllData( self, feedData, data ):
        for key in ( "title", "url", "date" ):
            if not data.has_key( key ):
                return False
        data[ "fileName" ] = self.getFileName( feedData, data )
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Add in extra data with defaults if they're not set up for the feed.
    def addExtraData( self, feedDict ):
        data = {}
        data[ "nameFormat" ] = feedDict.get( "nameFormat", "( title, dateFormat )" )
        data[ "dateFormat" ] = feedDict.get( "dateFormat", "%Y-%m-%d_%H-%M-%S" )
        data[ "seperator" ] = feedDict.get( "seperator", "-" )
        data[ "space" ] = feedDict.get( "space", "_" )
        data[ "startDate" ] = feedDict.get( "startDate", None )
        return data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Generator of all the nodes for 'items' e.g. each podcast.
    def genItems( self, doc ):
        return ( item
            for rss in doc.childNodes
                if utils.xmlFilterName( rss, "rss" )
                    for chan in rss.childNodes
                        if utils.xmlFilterName( chan, "channel" )
                            for item in chan.childNodes
                                if utils.xmlFilterName( item, "item" )
        )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Generator of all the nodes for 'items' e.g. each podcast.
    def getFileName( self, feedData, data ):
        dateFormat = data[ "date" ].strftime( feedData[ "dateFormat" ] )
        title = data[ "title" ].title()
        nameFormat = eval( "(%s)" % ( feedData[ "nameFormat" ], ) )
        seperator = feedData[ "seperator" ]
        name =  '%s%s%s' % ( nameFormat[ 0 ], seperator, nameFormat[ 1 ] )
        url = data[ "url" ]
        fileExtension = url[ url.rfind("."):]
        fileName = "%s%s" % ( name, fileExtension )
        fileName = fileName.replace(" %s " % seperator, seperator )
        fileName = fileName.replace( ", ", seperator ).replace( " ", "_")
        return fileName

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test run.
if __name__ == "__main__":
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Imports needed for test.
    from settingsJson import Settings, Config
    from grabber import Grabber
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Set up the Settings and them use FeedGrabber.
    settings = Settings( Config )
    grabber = Grabber( settings )
    scraper = Scraper( settings, grabber.xmls )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Print out the data.
    print "ITEMS:\n"
    print scraper.items
    print "DATA:\n"
    print scraper.data
