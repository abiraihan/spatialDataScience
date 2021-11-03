# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 14:19:33 2021

@author: ABIR RAIHAN
"""

import geopandas
import pandas
import collections

class readData:
    
    @classmethod
    def readExcel(
            cls,
            excelFilePath:str,
            sheetNames:str,
            **kwargs
            ):
        
        cls._excelFilePath = excelFilePath
        cls._sheetNames = sheetNames
        
        data_args = dict(
            shapeGeometry = 'Point',
            latAttributes = None,
            longAttributes = None,
            polyAttributes = None
            )
        fileInfo = collections.namedtuple(
            'fileInfo',
            ['filePath', 'sheetNames',
             'geometry', 'latiAttr',
             'longAttr', 'polyAttr']
            )
        
        for key, value in data_args.items():
            if key in kwargs: data_args[key] = kwargs[key]
        
        if not data_args['shapeGeometry'] in ['Point', 'Polygon']:
            raise ValueError("Only acceptable geometry can be created is Point or, Polygon")
        
        if data_args['latAttributes'] is None and data_args['shapeGeometry'] == 'Point':
            raise AttributeError(f"Please specify the Latitude attribute for {data_args['shapeGeometry']} geometry")
        
        if data_args['longAttributes'] is None and data_args['shapeGeometry'] == 'Point':
            raise AttributeError(f"Please specify the Longitude attribute for {data_args['shapeGeometry']} geometry")
        
        if data_args['polyAttributes'] is None and data_args['shapeGeometry'] == 'Polygon':
            raise AttributeError(f"Please specify the Polygon geometry attribute for {data_args['shapeGeometry']} geometry")
        
        dataFrame = pandas.read_excel(
            cls._excelFilePath,
            sheet_name = cls._sheetNames
            )
        if data_args['shapeGeometry'] == 'Point':
            geoData = geopandas.GeoDataFrame(
                dataFrame,
                geometry = geopandas.points_from_xy(
                    dataFrame[data_args['latAttributes']],
                    dataFrame[data_args['longAttributes']]),
                crs="EPSG:4326"
                )
        elif data_args['shapeGeometry'] == 'Polygon':
            geoData = geopandas.GeoDataFrame(
                dataFrame,
                geometry = dataFrame[data_args['polyAttributes']],
                crs="EPSG:4326"
                )
        else:
            raise ValueError("Only acceptable geometry can be created is Point or, Polygon")
        
        fileDesc = fileInfo(
            cls._excelFilePath, cls._sheetNames,
            data_args['shapeGeometry'], data_args['latAttributes'],
            data_args['longAttributes'], data_args['polyAttributes']
            )
        return geoData, fileDesc