# Copyright (c) 2019 Karol Babioch <karol@babioch.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import logging
import subprocess
import sys

# TODO
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class Chronyc:

    # TODO Implement parsing of rtcdata

    def chronyc(self, args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        # TODO Make path of chronyc configurable?
        # TODO Check for existence of chronyc
        chronyc = '/usr/bin/chronyc'
        cmdline = [chronyc, '-c'] + args
        logger.debug('Running: %s', cmdline)
        return subprocess.Popen(cmdline, stdin=stdin, stdout=stdout, stderr=stderr, encoding=sys.getdefaultencoding())

    def activity(self):
        #4,0,0,0,0
        reader = csv.reader(self.chronyc(['activity']).stdout)
        # TODO Check exit code, stderr, etc.
        keys = ['online', 'offline', 'burst_online', 'burst_offline', 'unresolved']
        values = next(reader)
        return dict(zip(keys, values))

    def tracking(self):
        #BC4424CB,188.68.36.203,3,1559341529.942906189,0.000017624,0.004522092,0.004522092,1.399,217.384,0.102,0.034927350,0.026541274,1.4,Normal
        reader = csv.reader(self.chronyc(['tracking']).stdout)
        # TODO Check exit code, stderr, etc.
        keys = ['ref', 'name', 'stratum', 'ref_time', 'current_correction',
                'last_offset', 'rms_offset', 'freq', 'residual_freq', 'skew',
                'root_delay', 'root_dispersion', 'update_interval', 'leap_status']
        values = next(reader)
        return dict(zip(keys, values))

    def sources(self):
        #^,*,188.68.36.203,2,8,377,163,0.001121406,0.001089684,0.055754013
        #^,+,213.251.53.187,2,8,377,166,0.000500402,0.000468858,0.048602168
        #^,+,78.46.107.140,2,8,377,166,-0.001950080,-0.001981611,0.056199428
        #^,+,5.45.111.220,2,7,377,30,-0.000580235,-0.000580235,0.044912908
        reader = csv.reader(self.chronyc(['sources']).stdout)
        # TODO Check exit code, stderr, etc.
        sources = []
        keys = ['mode', 'state', 'name', 'stratum', 'poll', 'reach', 'lastrx',
                'adjusted_offset', 'measured_offset', 'estimated_error']
        for row in reader:
            sources.append(dict(zip(keys, row)))
        return sources
