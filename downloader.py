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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
class Downloader:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Take the settings, feeds and filenames.
    def __init__( self, fileNames, lists ):
        self.fileNames = fileNames
        self.lists = lists
        self.reset()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def reset( self ):
        #self.downloadAll()
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def downloadAll( dryRun ):
        for key in priority:
            value = newDict.get( key, None)
            if not value:
                continue
            print "Downloading %s from: %s" %( len( value ), key )
            value.sort( reverse=True, key=lambda v: v[ "date" ] )
            for item in value:
                download( item[ "url" ], item[ "fullFilePath" ], verbose, dryRun )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def download( url, filePath, verbose, dryRun ):
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

