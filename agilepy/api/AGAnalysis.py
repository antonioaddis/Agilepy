"""
 DESCRIPTION
       Agilepy software

 NOTICE
       Any information contained in this software
       is property of the AGILE TEAM and is strictly
       private and confidential.
       Copyright (C) 2005-2020 AGILE Team.
           Addis Antonio <antonio.addis@inaf.it>
           Baroncelli Leonardo <leonardo.baroncelli@inaf.it>
           Bulgarelli Andrea <andrea.bulgarelli@inaf.it>
           Parmiggiani Nicolò <nicolo.parmiggiani@inaf.it>
       All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from agilepy.config.AgilepyConfig import AgilepyConfig
from agilepy.config.XMLconfig import SourcesConfig
from agilepy.utils.Utils import AgilepyLogger
from agilepy.parameters.Parameters import Parameters
from agilepy.api.ScienceTools import ctsMapGenerator, expMapGenerator, gasMapGenerator, intMapGenerator

class AGAnalysis:

    def __init__(self, configurationFilePath):

        self.config = AgilepyConfig(configurationFilePath)

        self.logger = AgilepyLogger(self.config.getConf("output","outdir"), self.config.getConf("output","logfilename"), self.config.getConf("output","debuglvl"), init=True)

        self.sourcesconfig = SourcesConfig("./agilepy/testing/demo/sourceconf.xml")

    def setOptions(self, **kwargs):

        rejected = self.config.setOptions(**kwargs)

        if rejected:

            self.logger.warning(self, "Some options have not been set: {}".format(rejected))

    def printOptions(self):

        self.config.printOptions()

    def generateMaps(self):

        fovbinnumber = self.config.getOptionValue("fovbinnumber")
        energybins = self.config.getOptionValue("energybins")

        initialFovmin = self.config.getOptionValue("fovradmin")
        initialFovmax = self.config.getOptionValue("fovradmax")

        initialMapNamePrefix = self.config.getOptionValue("mapnameprefix")

        for stepi in range(0, fovbinnumber):

            if fovbinnumber == 1:
                bincenter = 30
                fovmin = initialFovmin
                fovmax = initialFovmax
            else:
                bincenter, fovmin, fovmax = self.updateFovMinMaxValues(fovbinnumber, initialFovmin, initialFovmax, stepi+1)


            for stepe in energybins:

                if Parameters.checkEnergyBin(stepe):

                    emin = stepe[0]
                    emax = stepe[1]

                    skymapL = Parameters.getSkyMap(emin, emax)
                    skymapH = Parameters.getSkyMap(emin, emax)
                    mapNamePrefix = Parameters.getMapNamePrefix(emin, emax, stepi+1)

                    self.logger.info(self, "\n\nMap generation => fovradmin %s fovradmax %s bincenter %s emin %s emax %s mapNamePrefix %s skymapL %s skymapH %s", [fovmin,fovmax,bincenter,emin,emax,mapNamePrefix,skymapL,skymapH])

                    tools = [ctsMapGenerator, expMapGenerator, gasMapGenerator, intMapGenerator]

                    self.config.setOptions(mapnameprefix=initialMapNamePrefix+"_"+mapNamePrefix)
                    self.config.setOptions(fovradmin=fovmin, fovradmax=fovmax)
                    self.config.addOptions("selection", emin=emin, emax=emax)
                    self.config.addOptions("maps", skymapL=skymapL, skymapH=skymapH)

                    for tool in tools:
                        tool.setArguments(self.config)

                    self.config.addOptions("maps", expmap=expMapGenerator.outfilePath, ctsmap=ctsMapGenerator.outfilePath)

                    for tool in tools:
                        if not tool.allRequiredOptionsSet(self.config):
                            self.logger.critical(self,"Some options have not been set.")
                            exit(1)



                    for tool in tools:
                        tool.call()


                else:

                    self.logger.warning(self,"Energy bin [%s, %s] is not supported. Map generation skipped.", [stepe[0], stepe[1]])

    def mle(self):

        pass

    def updateFovMinMaxValues(self, fovbinnumber, fovradmin, fovradmax, stepi):

        # print("\nfovbinnumber {}, fovradmin {}, fovradmax {}, stepi {}".format(fovbinnumber, fovradmin, fovradmax, stepi))
        A = float(fovradmax) - float(fovradmin)
        B = float(fovbinnumber)
        C = stepi

        binleft =  ( (A / B) * C )
        binright = ( A / B  )
        bincenter = binleft - binright / 2.0
        fovmin = bincenter - ( A / B ) / 2.0
        fovmax = bincenter + ( A / B ) / 2.0

        # print("bincenter {}, fovmin {}, fovmax {}".format(bincenter, fovmin, fovmax))

        return bincenter, fovmin, fovmax
