#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PyCast. Authored by Nathan Ross Powell.
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
GotPodcast = "got"
NeedPodcast = "need"
WantPodcast = "want"
SkipPodcast = "skip"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get feed files from the net and save them off with a better name.
class Lister:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Take the settings, feeds and filenames.
    def __init__( self, setting, feeds, fileNames ):
        self.setting = setting
        self.feeds = feeds
        self.fileNames = fileNames
        self.lists = {}
        self.writeOutLists()
        self.reset()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Main setting of the Lister data. 
    def reset( self ):
        cache = self.setting.data[ "cache" ]
        for name, data in self.feeds.iteritems():
            folder = os.path.join( cache, self.fileNames[ name ] )
            listFile = os.path.join( folder, ListFile )
            podcasts = self.getListFileLines( folder ) 
            feedList = self.feedIndexer( folder, name, data, podcasts )
            self.lists[ name ] = feedList

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # List all of the feed entries and their state ( ignore, had, got, need ).
    def feedIndexer( self, folder, name, data, podcasts ):
        feedList = []
        for item in self.feeds[ name ]:
            print item
            podcast = os.path.join( folder, item[ "fileName" ] )
            if utils.fileExists( podcast ):
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

    def getListFileLines( self, folder ):
        listFile = os.path.join( folder, ListFile )
        try:
            with open( listFile, 'r' ) as feedListFile:
                return feedListFile.read().splitlines()
        except:
            return []
    def updateListFile( self, folder, podcasts ):
        listFile = os.path.join( folder, ListFile )
        with open( listFile, 'w' ) as feedListFile:
            feedListFile.writelines( map(lambda x:"%s\n" % (x,), podcasts ) ) 

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Merge stored list with the current downloaded files.
    def writeOutLists( self ):
        root = self.setting.data[ "folder" ]
        for name, data in self.feeds.iteritems():
            folder = os.path.join( root, self.fileNames[ name ] )
            # If the folders not there, no need to update the file.
            if not os.path.exists( folder ):
                continue
            listFile = os.path.join( folder, ListFile )
            podcasts = self.getListFileLines( folder ) 
            numPodcasts = len( podcasts ) 
            for file in os.listdir( folder ):
                if file not in podcasts:
                    podcasts.append( file )
            if len( podcasts ) > numPodcasts:
                self.updateListFile( folder, podcasts ) 

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
            print "  Pod:", podcast
