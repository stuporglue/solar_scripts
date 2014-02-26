#!/usr/bin/env python
# coding=UTF-8

# From: http://resources.arcgis.com/en/help/main/10.1/index.html#//009z000000tm000000

# http://webhelp.esri.com/arcgisdesktop/9.2/index.cfm?TopicName=Calculating_solar_radiation
# http://resources.arcgis.com/en/help/main/10.2/index.html#/Area_Solar_Radiation/009z000000t5000000/
# Default is 8x8

# This class provides a sunmap
class sunmap:

    NOINTERVAL  = 'nointerval'
    INTERVAL    = 'interval'

    UNIFORM_SKY = 'uniform_sky'
    STANDARD_OVERCAST_SKY = 'standard_overcast_sky'

    def __init__(self):
        self._sky_size = [200,200]
        self._days = self.TimeMultiDays(2014,5,160)
        self._day_interval = 14
        self._hour_interval = 0.5
        self._each_interval = NOINTERVAL
        self._z_factor = 1
        self._calculation_directions = 32
        self._zenith_divisions = 8
        self._azimuth_divisions = 8
        self._difuse_model_type = STANDARD_OVERCAST_SKY
        self._diffuse_proportion = 0.3
        self._transmittivity = 0.5
        # self._out_diffuse_radiation_raster = ??
        # self._out_direct_duration_raster = ??

    # Returns an array of this sunmap's sectors
    def sectors():
        # To calculate 
        # diffuse radiation for a particular location, a skymap is created to represent 
        # a hemispherical view of the entire sky divided into a series of sky sectors 
        # defined by zenith and azimuth angles. Each sector is assigned a unique identifier 
        # value, along with the centroid zenith and azimuth angles. Diffuse radiation is 
        # calculated for each sky sector based on direction (zenith and azimuth).

        # The figure below is a skymap with sky sectors defined by 8 zenith divisions and 
        # 16 azimuth divisions. Each color represents a sky sector, or portion of the sky, 
        # from which diffuse radiation originates. 

        azmuthdivsize = 360 / self._azimuth_divisions
        azmuthangles = range(0,360,azmuthdivsize)

        zenithdivsize = 180 / self._zenith_divisions
        zenithangles = range(-90,90,zenithdivsize)

        sectors = []

        for aa in azmuthangles:
            for za in zenithangles:
                sectors.push({'azmuth':aa,'zenith':za})

        return sectors

    def transmissivity():
        return self._transmittivity



     


    # Not sure if these are helpful at all....
    def zenithAngle(local_latitude,upsidedown_q,hour_angle):
        coszenith = amath.sin(local_latitude) * math.sin(upsidedown_q) + math.cos(local_latitude) * math.cos(upsidedown_q) * math.cos(hour_angle)
        return math.acos(coszenith)

    def solarElevationAngle(hour_angle,upsidedown_q,local_latitude):
        sinalpha = math.cos(hour_angle) * math.cos(upsidedown_q) * math.cos(local_latitude) + math.sin(upsidedown_q) * math.sin(local_latitude)
        return math.asin(sinalpha)

    def sunriseSet(o_thing,upsidedown_q):
        cosh = -1 * math.tan(o_thing) * math.tan(upsidedown_q)
        return math.acos(cosh)


