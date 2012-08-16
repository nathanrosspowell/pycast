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
from lister import * 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Globals.

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
class Downloader:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Take the settings, feeds and filenames.
    def __init__( self, setting, lists, data ):
        self.setting = setting
        self.lists = lists
        self.data = data
        self.reset()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def reset( self ):
        #self.downloadAll()
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def downloadAll( self, verbose, dryRun ):
        for name, items in self.lists.iteritems():
            sortedItems = sorted( 
                items, 
                reverse=True, 
                key=lambda v:self.data[ v["name"] ][ v["title"] ][ "date" ]
            )
            root = self.setting.data[ "folder" ]
            folder = self.setting.data[ "feeds" ][ name ][ "folder" ]
            feedFolder = os.path.join( root, folder )
            for item in sortedItems:
                if item[ "status" ] == NeedPodcast:
                    self.download( item, feedFolder, verbose, dryRun )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def download( self, item, feedFolder, verbose, dryRun ): 
        url = item[ "podcast" ]
        filePath = os.path.join( feedFolder, item[ "fileName" ] )
        if not os.path.exists( feedFolder ):
            os.makedirs( feedFolder )
        print "\tStarting", url, "as", filePath, "..."
        if os.path.isfile( filePath ):
            print "File already exists: %s" % ( filePath, )
        else:
            try:
                if not dryRun:
                    urllib.urlretrieve( url, filePath )
                else:
                    with open( filePath, 'w' ) as dummy:
                        dummy.write( url )
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
    lister = Lister( settings, scraper.items )
    downloader = Downloader( settings, lister.lists, scraper.items )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Print out the data.
    downloader.downloadAll( True, True )

