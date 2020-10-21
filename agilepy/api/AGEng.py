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

import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.io import fits
from os.path import join
from pathlib import Path

from agilepy.config.AgilepyConfigEng import AgilepyConfigEng
from agilepy.utils.PlottingUtils import PlottingUtils
from agilepy.utils.AgilepyLogger import AgilepyLogger
from agilepy.utils.AstroUtils import AstroUtils
from agilepy.utils.CustomExceptions import WrongCoordinateSystemError

class AGEng:
    """This class contains the high-level API methods you can use to run engineering analysis.

    This class requires you to setup a ``yaml configuration file`` to specify the software's behaviour.

    Class attributes:

    Attributes:
        config (:obj:`AgilepyConfigEng`): it is used to read/update configuration values.
        logger (:obj:`AgilepyLogger`): it is used to log messages with different importance levels.
    """

    def __init__(self, configurationFilePath):
        """AGEng constructor.

        Args:
            configurationFilePath (str): the relative or absolute path to the yaml configuration file.

        Example:
            >>> from agilepy.api import AGEng
            >>> ageng = AGEng('agconfig.yaml')

        """

        self.config = AgilepyConfigEng()

        self.config.loadConfigurations(configurationFilePath, validate=True)

        self.outdir = join(self.config.getConf("output","outdir"), "eng_data")

        Path(self.outdir).mkdir(parents=True, exist_ok=True)

        self.logger = AgilepyLogger()

        self.logger.initialize(self.outdir, self.config.getConf("output","logfilenameprefix"), self.config.getConf("output","verboselvl"))

        self.plottingUtils = PlottingUtils(self.config, self.logger)
