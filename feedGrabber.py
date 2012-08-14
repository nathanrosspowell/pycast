#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
import xml.dom.minidom
import urllib
import os
# Local.
import utils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get feed files from the net and save them off with a better name. 
class FeedGrabber:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__( self, setting ):
        self.feeds = setting.data[ "feeds" ] 
        self.setting = setting
        # A dict of names -> feed names.
        self.fileNames = {}
        # Make a dict of names -> xml
        self.xmls = {} 
        for name, data in self.feeds.items():
            fileName = self.feedNamer( name ) 
            path = self.feedOpener( setting, fileName, data )
            self.xmls[ name ] = self.feedReader( path )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Open and save a file to disk.
    def feedNamer( self, name ):
        fileName = utils.slugify( name ) 
        self.fileNames[ name ] = fileName
        return fileName
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
        feedPath = "%s.feed" % ( os.path.join( cache, name ), ) 
        try:
            # Save the rss into our new feedName.feed file.
            opener.retrieve( rss, feedPath )
        except:
            print "Could not retrieve file %s." % ( name, )
        return feedPath

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Open and save a file to disk.
    def feedReader( self, path ):
        # Once it's saved, we can then open it and get the data.
        with open( path, 'r' ) as rssXml:
            # Return the xml doc. 
            print ">>>>>>>>>>>\n", rssXml
            return  xml.dom.minidom.parse( rssXml )
        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test run.
if __name__ == "__main__":
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Imports needed for test. 
    from settingsJson import Settings
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Set up the Settings and them use FeedGrabber.
    settings = Settings( "config.json" )
    feedGraber = FeedGrabber( settings )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Print out the data. 
    print feedGraber.feeds
    print feedGraber.xmls
