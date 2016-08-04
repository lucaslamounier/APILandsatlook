# -*- coding: UTF-8 -*-
"""
/***************************************************************************
Name                 : ApiLandsatlook
Description          : ApiLandsatlook api to get data from usgs landsatlook
Date                 : August, 2016
copyright            : (C) 2016 by Lucas Lamounier
email                : lucasls.oas@gmail.com
****************************************************************************/
Basic usage
****************************************************************************
    api = ApiLandsatlook()
    api.query(start_date='2015-01-01', end_date='2016-12-31', cloudCover='40', xmin='-6366732.060713638',
              ymin='-377242.91314659826', xmax='-5877535.079688745', ymax='-137230.64433126024')
    products = api.get_products()
    bbox = [-6366732.060713638, -377242.91314659826, -5877535.079688745, -137230.64433126024]
    png_url = api.get_processed_image_png(bbox=bbox, contrast='stretch')
"""


import requests
import datetime
try:
    from urlparse import urljoin
except:
    from urllib.parse import urljoin

def convert_timestamp_to_datetime(miliseconds):
    return datetime.datetime.fromtimestamp(miliseconds)


class ApiLandsatlook(object):

    base_url = 'http://landsatlook.usgs.gov/arcgis/rest/services/LandsatLook/ImageServer/query?f=json&where='
    base_url_export_image = 'http://landsatlook.usgs.gov/arcgis/rest/services/LandsatLook/ImageServer/exportImage' \
                            '?f=image&format=png&renderingRule='
    sensors = ['OLI', 'ETM_SLC_OFF', 'ETM', 'TM', 'MSS']

    def get_sensors(self, sensors=None):
        """
            :return the parameter according to the sensor
        """
        if sensors and not isinstance(sensors, list):
            print("The sensors must be a list , for example: ['OLI', 'ETM_SLC_OFF']")
            exit(0)
        if not sensors:
            sensors = self.sensors
        param = "AND ("
        for sensor in sensors:
            if param.find('sensor') != -1:
                param += "OR sensor = '{}' ".format(sensor)
            else:
                param += "sensor = '{}' ".format(sensor)
        param = param[:-1] + ') '
        return param

    def format_date(self, start_date, end_date):
        if not isinstance(start_date, str) or not isinstance(end_date, str):
            print("The start_date and end_date should be of the form example: '2016-01-01' ")
            exit(0)
        params = "(acquisitionDate >= date'{}' AND acquisitionDate <= date'{}') " \
                 "AND (dayOfYear >=1 AND  dayOfYear <= 366)"
        return params.format(start_date, end_date)

    def format_url(self, start_date, end_date, cloudCover, xmin, ymin, xmax, ymax):
        """
            :return format url for query
        """
        params_date = self.format_date(start_date, end_date)
        params_sensors = self.get_sensors()
        params_cloud = "AND (cloudCover <= {})&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=".format(cloudCover)
        params_geometry = "{'xmin': %s,'ymin':%s,'xmax':%s,'ymax':%s,'spatialReference':{'wkid':102100}}" % (xmin, ymin, xmax, ymax)
        other_params = "&geometryType=esriGeometryEnvelope&inSR=102100&outFields=sceneID,sensor,acquisitionDate," \
                       "dateUpdated,path,row,PR,cloudCover,sunElevation,sunAzimuth,receivingStation,sceneStartTime," \
                       "month,year,OBJECTID,dayOfYear,dayOrNight,browseURL&orderByFields=acquisitionDate&outSR=102100"
        self.url = '{0}{1}{2}{3}{4}{5}'.format(self.base_url, params_date, params_sensors, params_cloud, params_geometry, other_params)

    def show_url(self):
        """
            :return show url of query
        """
        return self.url

    def get_content(self):
        """
            :return api call to ladsatlook
        """
        response = requests.get(self.url)
        return response

    def query(self, start_date, end_date, cloudCover, xmin, ymin, xmax, ymax):
        """
            :return performs image query
        """
        self.format_url(start_date, end_date, cloudCover,xmin, ymin, xmax, ymax)
        self.content = self.get_content()
        if self.content.status_code != 200:
            print('Api returned %s error' % self.content.status_code)
            exit(0)

    def get_products(self):
        """
            :return all the images according to the query
        """
        self.products = self.content.json()['features']
        print('[%s images found]' % len(self.products))
        if len(self.products) < 1:
            return []
        return self.products

    def get_params_contrast(self, contrast):
        """
            :returns the parameter according to contrast
        """
        if contrast == 'stretch':
            param =  "{'rasterFunction':'Stretch','rasterFunctionArguments':{'StretchType':3,'NumberOfStandardDeviations':3,'DRA':true},"\
                     "'variableName':'Raster'}&mosaicRule={'mosaicMethod':'esriMosaicLockRaster','ascending':true,"
        elif contrast == 'clip':
            param = "{'rasterFunction':'Stretch','rasterFunctionArguments':{'StretchType':6,'MinPercent':0.5,'MaxPercent':0.5,'DRA':true},"\
                    "'variableName':'Raster'}&mosaicRule={'mosaicMethod':'esriMosaicLockRaster','ascending':true,"
        return param

    def get_lock_raster_ids(self):
        """ GET LAST 10 IMAGES"""
        last_items = self.products[-11:]
        raster_ids = []
        for item in last_items:
            raster_ids.append(item['attributes']['OBJECTID'])
        return raster_ids

    def format_url_export_image(self, params_contrast, raster_ids, bbox):
        """
            :return url formated for get image processed
        """
        params_raster_ids = "'lockRasterIds': %s,'mosaicOperation':'MT_FIRST'}&" % (str(raster_ids))
        params_bbox = "bbox="
        for bbx in bbox:
            params_bbox += '{},'.format(bbx)
        params_bbox = "{}&imageSR=102100&bboxSR=102100&size=1600,785".format(params_bbox[:-1])
        url_png = "{0}{1}{2}{3}".format(self.base_url_export_image,params_contrast, params_raster_ids, params_bbox)
        return url_png

    def get_processed_image_png(self, bbox, contrast=None):
        """
            @:param bbox: [-6366732.060713638,-377242.91314659826,-5877535.079688745,-137230.64433126024]
            @:param contrast: 'stretch' or 'clip'
            :return url of image png
        """
        if contrast and contrast not in ['stretch', 'clip']:
            print("Error contrast not found, allowed contrasts ['stretch', 'clip'] ")
            exit(1)

        if not contrast:
            contrast = 'stretch'

        if not isinstance(bbox, list):
            print("bbox must be exaple: ['-6366732.060713638','-377242.91314659826','-5877535.079688745','-137230.6443312602']")
            exit(1)

        params_contrast = self.get_params_contrast(contrast)
        raster_ids = self.get_lock_raster_ids()
        url = self.format_url_export_image(params_contrast, raster_ids, bbox)
        return url

    def __repr__(self):
        return '<APILandsatLook>'