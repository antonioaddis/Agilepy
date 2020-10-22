# DESCRIPTION
#       Agilepy software
#
# NOTICE
#      Any information contained in this software
#      is property of the AGILE TEAM and is strictly
#      private and confidential.
#      Copyright (C) 2005-2020 AGILE Team.
#          Baroncelli Leonardo <leonardo.baroncelli@inaf.it>
#          Addis Antonio <antonio.addis@inaf.it>
#          Bulgarelli Andrea <andrea.bulgarelli@inaf.it>
#          Parmiggiani Nicolò <nicolo.parmiggiani@inaf.it>
#      All rights reserved.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import List
import numbers

from agilepy.utils.Utils import Utils

class CompletionStrategies:

    
    @staticmethod
    def _glonDeltaIncrement(confDict):
        confDict["selection"]["glon"] += 0.000001

    @staticmethod
    def _convertEnergyBinsStrings(confDict):

        l = []
        for stringList in confDict["maps"]["energybins"]:
            res = Utils._parseListNotation(stringList)
            l.append([int(r) for r in res])
        confDict["maps"]["energybins"] = l

    @staticmethod
    def _convertBackgroundCoeff(confDict, bkgCoeffName):

        bkgCoeffVal = confDict["model"][bkgCoeffName]
        numberOfEnergyBins = len(confDict["maps"]["energybins"])
        fovbinnumber = confDict["maps"]["fovbinnumber"]
        numberOfMaps = numberOfEnergyBins*fovbinnumber

        if bkgCoeffVal is None:
            confDict["model"][bkgCoeffName] = [-1 for i in range(numberOfMaps)]

        # if -1
        elif bkgCoeffVal == -1:
            confDict["model"][bkgCoeffName] = [-1 for i in range(numberOfMaps)]

        # if only one value
        elif isinstance(bkgCoeffVal, numbers.Number):
            confDict["model"][bkgCoeffName] = [bkgCoeffVal]

        # if comma separated values
        elif isinstance(bkgCoeffVal, str):
            confDict["model"][bkgCoeffName] = Utils._parseListNotation(bkgCoeffVal)

        # if List
        elif isinstance(bkgCoeffVal, List):
            confDict["model"][bkgCoeffName] = bkgCoeffVal

        else:
            print(f"Something's wrong..bkgCoeffName: {bkgCoeffName}, bkgCoeffVal: {bkgCoeffVal}")
            confDict["model"][bkgCoeffName] = None

    @staticmethod
    def _extendBackgroundCoeff(confDict):
        numberOfEnergyBins = len(confDict["maps"]["energybins"])
        fovbinnumber = confDict["maps"]["fovbinnumber"]
        numberOfMaps = numberOfEnergyBins*fovbinnumber

        while(len(confDict["model"]["isocoeff"])<numberOfMaps):
            confDict["model"]["isocoeff"].append(-1)

        while(len(confDict["model"]["galcoeff"])<numberOfMaps):
            confDict["model"]["galcoeff"].append(-1)




    @staticmethod
    def _setPhaseCode(confDict):

        if not confDict["selection"]["phasecode"]:
            if confDict["selection"]["tmax"] >= 182692800.0:
                confDict["selection"]["phasecode"] = 6 #SPIN
            else:
                confDict["selection"]["phasecode"] = 18 #POIN

    @staticmethod
    def _setTime(confDict):
        if confDict["selection"]["timetype"] == "MJD":
            confDict["selection"]["tmax"] = AstroUtils.time_mjd_to_tt(confDict["selection"]["tmax"])
            confDict["selection"]["tmin"] = AstroUtils.time_mjd_to_tt(confDict["selection"]["tmin"])
            confDict["selection"]["timetype"] = "TT"

    @staticmethod
    def _setExpStep(confDict):
        if not confDict["maps"]["expstep"]:
             confDict["maps"]["expstep"] = round(1 / confDict["maps"]["binsize"], 2)

    @staticmethod
    def _expandOutdirEnvVars(confDict):
        confDict["output"]["outdir"] = Utils._expandEnvVar(confDict["output"]["outdir"])

    @staticmethod
    def _expandEvtfileEnvVars(confDict):
        confDict["input"]["evtfile"] = Utils._expandEnvVar(confDict["input"]["evtfile"])

    @staticmethod
    def _expandLogfileEnvVars(confDict):
        confDict["input"]["logfile"] = Utils._expandEnvVar(confDict["input"]["logfile"])


    @staticmethod
    def _transformLoccl(confDict):

        userLoccl = confDict["mle"]["loccl"]

        if userLoccl == 99:
            confDict["mle"]["loccl"] = 9.21034
        elif userLoccl == 95:
            confDict["mle"]["loccl"] = 5.99147
        elif userLoccl == 68:
            confDict["mle"]["loccl"] = 2.29575
        else:
            confDict["mle"]["loccl"] = 1.38629