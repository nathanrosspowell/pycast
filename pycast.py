#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PyCast. Authored by Nathan Ross Powell.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
# Local.
import utils
from settingsJson import Settings, Config
from grabber import Grabber
from scraper import Scraper
from lister import Lister
from downloader import Downloader 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main class for the podcast downloader.
class PyCast:
    def __init__( self, configFile ):
        self.configFile = configFile
        self.reset()

    def reset( self ):
        self.setting = Settings( self.configFile )
        self.grabber = Grabber( self.setting )
        self.scraper = Scraper(
            self.setting, 
            self.grabber.xmls 
        )
        self.lister = Lister( 
            self.setting, 
            self.scraper.items, 
            self.grabber.fileNames 
        )
        self.downloader = Downloader( 
            self.lister.fileNames, 
            self.lister.lists
        )

    def download( self ):
        self.downloader.downloadAll()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main execution loop below.
if __name__ == "__main__":
    pyCast = PyCast( Config )
    print pyCast.grabber.xmls
    print pyCast.scraper.data
    print pyCast.lister.lists
    #pyCast.download()

