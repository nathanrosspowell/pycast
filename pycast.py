#!/usr/bin/python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports.
# Local.
import utils
from settingsJson import Settings, Config
from grabber import Grabber
from scraper import Scraper
from lister import Lister

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main class for the podcast downloader.
class PyCast:
    def __init__( self, configFile ):
        self.setting = Settings( configFile )
        self.grabber = Grabber( self.setting )
        self.scraper = Scraper( self.setting, self.grabber.xmls )
        self.lister = Lister( self.setting, self.scraper.data )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main execution loop below.
if __name__ == "__main__":
    pyCast = PyCast( Config )
    print pyCast.grabber.xmls
    print pyCast.scraper.data
    print pyCast.lister.lists

