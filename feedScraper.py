#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
# Local.
import utils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Turn the xml file into usable data. 
class FeedScraper:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__( self, setting, xmls ):
        self.xmls = xmls 
        self.data = {}
        for name, data in self.xmls.items():
            self.data[ name ] = []
            for item in self.feedSanitise( setting, data ):
                self[ name ].append( )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Turn the xml into an easy to use python object.
    def feedSanitise( self, settings, xml ):
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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #  Check the esential data is there.
    def gotAllData( self, data ):
        for key in ( "title", "url", "date" ):
            if not data.has_key( key ):
                return False
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Add in extra data with defaults if they're not set up for the feed. 
    def addExtraData( self, data, feedDict):
        data[ "nameFormat" ] = feedDict.get( "nameFormat", "( title, dateFormat )" )
        data[ "dateFormat" ] = feedDict.get( "dateFormat", "%Y-%m-%d_%H-%M-%S" )
        data[ "seperator" ] = feedDict.get( "seperator", "-" )
        data[ "space" ] = feedDict.get( "space", "_" )
        data[ "startDate" ] = feedDict.get( "startDate", None )
        data[ "fileName" ] = getFileName( data )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Generator of all the nodes for 'items' e.g. each podcast. 
    def genNodes( self, doc ):
        return ( item
            for rss in doc.childNodes 
                if filterName( rss, "rss" )
                    for chan in rss.childNodes
                        if filterName( chan, "channel" )
                            for item in chan.childNodes
                                if filterName( item, "item" ) 
        )
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
    feedGraber = FeedGrabber( settings )
    feedScraper = FeedScraper( settings, feedGrabber.xmls )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Print out the data. 
    print feedScraper.data
