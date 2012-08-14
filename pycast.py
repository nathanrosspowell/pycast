#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
# Local.
import utils
from settingsJson import Settings
from feedGrabber import FeedGrabber
from feedScraper import FeedScraper
from feedLister import FeedLister

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main class for the podcast downloader.
class PyCast:
    def __init__( self, configFile ):
        self.setting = Settings( configFile )
        self.grabber = FeedGrabber( self.setting )
        self.scraper = FeedScraper( self.setting, self.grabber.xmls )
        self.lister = FeedLister( self.setting, self.scraper.data ) 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main execution loop below. 
if __name__ == "__main__":
    pyCast = PyCast( "config.json" )
    print pyCast.grabber.xmls
    print pyCast.scraper.data
    print pyCast.lister.lists

