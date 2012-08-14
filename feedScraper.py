#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
from datetime import datetime
import time
# Local.
import utils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Turn the xml file into usable data.
class FeedScraper:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__( self, setting, xmls ):
        self.xmls = xmls
        self.data = {}
        for name, xml in self.xmls.iteritems():
            self.data[ name ] = []
            feedDict = setting.data[ "feeds" ][ name ]
            for data in self.feedSanitise( setting, xml, feedDict ):
                self.data[ name ].append( data )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Turn the xml into an easy to use python object.
    def feedSanitise( self, settings, xml, feedDict ):
        for itemNode in self.genItems( xml ):
            data = self.itemDict( itemNode )
            if self.gotAllData( data ):
                self.addExtraData( data, feedDict )
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
    def gotAllData( self, data ):
        for key in ( "title", "url", "date" ):
            if not data.has_key( key ):
                return False
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Add in extra data with defaults if they're not set up for the feed.
    def addExtraData( self, data, feedDict ):
        data[ "nameFormat" ] = feedDict.get( "nameFormat", "( title, dateFormat )" )
        data[ "dateFormat" ] = feedDict.get( "dateFormat", "%Y-%m-%d_%H-%M-%S" )
        data[ "seperator" ] = feedDict.get( "seperator", "-" )
        data[ "space" ] = feedDict.get( "space", "_" )
        data[ "startDate" ] = feedDict.get( "startDate", None )
        data[ "fileName" ] = self.getFileName( data )

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
    def getFileName( self, data ):    
        dateFormat = data[ "date" ].strftime( data[ "dateFormat" ] )
        title = data[ "title" ].title()
        nameFormat = eval( "(%s)" % ( data[ "nameFormat" ], ) )
        seperator = data[ "seperator" ]
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
    from settingsJson import Settings
    from feedGrabber import FeedGrabber
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Set up the Settings and them use FeedGrabber.
    settings = Settings( "config.json" )
    feedGrabber = FeedGrabber( settings )
    feedScraper = FeedScraper( settings, feedGrabber.xmls )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Print out the data.
    print feedScraper.data
