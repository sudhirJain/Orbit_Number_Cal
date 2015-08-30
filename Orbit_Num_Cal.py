#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------

Modifications by : Sudhir Jain
Date             : Jan 12, 2015
Descripition:    : New Class NPP_Orbit has been added in the code for retrieving Orbit Numbers
                   for NPP data and the data is packaged.The script runs on python2.7 as 
                   pyorbital module is compatable with python2.7.  Tracking Satellite can
                   changed and its Orbit Number can be retrieved.

#-------------------------------------------------------------------------------------------

import sys
import os
import commands

#-------------------------------------------------------------------------------------------
#     Following parameters and code has been in serted to cacluate NPP orbhit numbers.
#-------------------------------------------------------------------------------------------

from datetime import timedelta, datetime
import ephem
import math
import time
from pyorbital.orbital import Orbital

#-------------------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------------------

IN_TLE_DIR           = '/station/data/TLE/'
IN_TLE_FILE          = IN_TLE_DIR+'tles.txt'
TRK_SATELLITE        = 'SUOMI NPP'
EARTH_STATION_LONG   = '133 54'
EARTH_STATION_LAT    = '-23 42'

class NPP_Orbit:

# Constructor of NPP_Orbit

    def __init__(self):

        self.ground_lat     =  EARTH_STATION_LAT
        self.ground_long    =  EARTH_STATION_LONG
        self.observer       =  ephem.Observer()
        self.observer.lat   =  self.ground_lat
        self.observer.long  =  self.ground_long
        self.observer.date  =  datetime.utcnow()
        self.tle            =  IN_TLE_FILE
        self.tles           =  []
        self.satellite_name =  TRK_SATELLITE
        self.orb            =  Orbital(self.satellite_name,tle_file=self.tle)

# Functions

    def read_tle(self):
        self.tles = open(self.tle, 'r').readlines()
        self.tles = [item.strip() for item in self.tles]
        self.tles = [(self.tles[i], self.tles[i+1], self.tles[i+2]) \
                for i in xrange(0, len(self.tles)-2, 3)]
        return

    def get_pass_num_t(self,yyyy,mm,dd,hh,mn,ss):
        indate = str(yyyy) + '-' + str(mm) + '-' +str(dd) + ' ' +\
                str(hh) + ':' + str(mn) + ':' + str(ss)
        self.observer.date  =  indate
        for tle in self.tles:
                if tle[0].strip() == self.satellite_name:
                        sat = ephem.readtle(tle[0],tle[1],tle[2])
                        rt, ra, tt, ta, st, sa = self.observer.next_pass(sat)
                        num = self.orb.get_orbit_number(datetime.strptime(str(tt), "%Y/%m/%d %H:%M:%S"),tbus_style=True)

        return num

    def __del__(self):
        pass

#-------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------
