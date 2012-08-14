#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
import xml.dom.minidom
import urllib
import os
# Local.
import utils
from settingsJson import Settings

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get feed files from the net and save them off with a better name. 
class FeedGrabber:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__( self, setting ):
        self.feeds = setting.data[ "feeds" ] 
        self.setting = setting
        self.xmls ={} 
        # Make a dict of feed names -> xml
        for name, data in self.feeds.items():
            self.xmls[ name ] = self.feedOpener( setting, name, data )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Open and save a file to disk.
    def feedOpener( self, settings, name, data ):
        rss = data[ "rss" ]
        cache = settings.data[ "cache" ]
        # Use the fancy url opener.
        opener = urllib.FancyURLopener({})
        # Make sure the cache folder is there.
        if not os.path.exists( cache ):
            os.makedirs( cache )
        # Use a slug of the feed name for the new file to get saved.
        feedName = utils.slugify( name ) 
        feedPath = "%s.feed" % ( os.path.join( cache, feedName ), ) 
        # Save the rss into our new feedName.feed file.
        opener.retrieve( rss, feedPath )
        # Once it's saved, we can then open it and get the data.
        with open( feedPath, 'r' ) as rssXml:
            # Return the xml doc. 
            return  xml.dom.minidom.parse( rssXml )
        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test run.
if __name__ == "__main__":
    settings = Settings( "config.json" )
    feedGraber = FeedGrabber( settings )
    print feedGraber.feeds
    print feedGraber.xmls
