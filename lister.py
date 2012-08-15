#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
import xml.dom.minidom
import urllib
import os
# Local.
import utils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Globals.
ListFile = "podcasts.txt"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get feed files from the net and save them off with a better name.
class Lister:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__( self, setting, feeds, fileNames ):
        self.feeds = feeds
        self.fileNames = fileNames
        self.lists = {}
        cache = setting.data[ "cache" ]
        for name, data in self.feeds.iteritems():
            folder = os.path.join( cache, fileNames[ name ] )
            listFile = os.path.join( folder, ListFile )
            try:
                with open( listFile, 'r' ) as feedListFile:
                    podcasts = feedListFile.readlines()
            except:
                podcasts = []
            feedList = self.feedIndexer( folder, name, data, podcasts )
            self.lists[ name ] = feedList

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # List all of the feed entries and their state ( ignore, had, got, need ).
    def feedIndexer( self, folder, name, data, podcasts ):
        feedList = []
        for item in self.feeds[ name ]:
            print item
            podcast = os.path.join( folder, item[ "fileName" ] )
            if os.path.exists( podcast ):
                status = "got"
            elif podcast in podcasts:
                status = "had"
            else:
                status = "need"
            feedList.append( {
                "podcast" : podcast,
                "status"  : status,
            } )
        return feedList




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test run.
if __name__ == "__main__":
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Imports needed for test.
    from settingsJson import Settings, Config
    from grabber import Grabber
    from scraper import Scraper
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Set up the Settings and them use FeedGrabber.
    settings = Settings( Config )
    grabber = Grabber( settings )
    scraper = Scraper( settings, grabber.xmls )
    lister = Lister( settings, scraper.items, grabber.fileNames )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Print out the data.
    for name, podcasts in lister.lists.iteritems():
        print "Name:", name
        for podcast in podcasts:
            print "\tPod:", podcast
