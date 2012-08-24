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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 
    def fullReset( self ):
        self.setting = Settings( self.configFile )
        self.grabber = Grabber( self.setting )
        self.scraper = Scraper(
            self.setting, 
            self.grabber.xmls 
        )
        self.lister = Lister( 
            self.setting, 
            self.scraper.items
        )
        self.downloader = Downloader( 
            self.setting,
            self.lister.lists,
            self.scraper.items
        )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 
    def download( self, verbose = False, dryRun = False ):
        self.downloader.downloadAll( verbose, dryRun )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main execution loop below.
if __name__ == "__main__":
    pyCast = PyCast( Config )
    pyCast.fullReset()
    pyCast.download( True, True )
    #pyCast.download()

