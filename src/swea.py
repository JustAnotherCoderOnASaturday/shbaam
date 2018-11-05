#!/usr/bin/env python
#shbaam_swea.py

#Purpose:




#*******************************************************************************
#Import Python modules
#*******************************************************************************
import sys
import netCDF4
import fiona
import shapely.geometry
import shapely.prepared
import math
import rtree

def check_command_line(sys.argv):
    ##Checks the length of arguements and if input files exist
    IS_arg = len(sys.argv)
    if IS_arg != 7:
        print('ERROR - 6 and only 6 arguments can be used')
        raise SystemExit(22) 

    for shb_file in sys.argv[1:3]:
	try:
            with open(shb_file) as file:
	        pass
	except IOError as e:
            print('ERROR - Unable to open ' + shb_file)
            raise SystemExit(22) 


def readFile():
    print('Read GLD netCDF file')
    return cdfFile

def createShapeFile(gld_dim_lat_length, gld_dim_lon_length,gld_dim_lon_length, lon_dimension_array, gld_lat_length_dimension_array, polygonShapeFile):
    shapeFile_Driver= polygonShapeFile.driver
    shapeFile_Point = shapeFile_Driver
    
    shapeFile_cells = polygonShapeFile.crs
    shapeFile_crs   = shapeFile_cells.copy()

	##Kept the same names, just in case
    shapeFile_schema= {'geometry':'Point',
			'properties':{
					'JS_gld_lon': 'int:4'
					'JS_gld_lat': 'int:4'}}

 
    with fiona.open(output_pnt_shp, 'w', driver=shapeFile_Point, \
			crs=shapeFile_cells,
			schema=shapeFile_schema) as pointFile:        
	for JS_gld_lon in range(gld_dim_lon_length):
	    gld_lon = gld_lon_dimension_array[JS_gld_lon]
	    if (gld_lon > 180):
		#Shifts GLD range [0:360] to [-180:180]
		gld_lon -= 180
	    for JS_gld_lat in range(gld_dim_lat_length):
		gld_lat = gld_dim_lat_length[JS_gld_lat]
		shapeFilePoint_Prepared={'JS_gld_lon':JS_gld_lon,
					'JS_gld_lat':JS_gld_lat}
		shapeFilePoint_geometry=shapely.geometry.mapping(\
			shapely.geometry.Point( (gld_lon, gld_lat) ))
		pointFile.write({
			'properties': shapeFilePoint_Prepared,
			'geometry'  : shapeFilePoint_geometry,
			})
				
    print(' - New ShapeFile Created')


def createSpatialIndex(pointFile):
    print('Create spatial index for the bounds of each point feature')
    index = rtree.index.Index()
    
    for feature in pointFile:
	feature_id = int(feature['id'])
    	#the first argument of index.insert has to be 'int', not 'long' or 'str'
    	shape=shapely.geometry.shape(feature['geometry'])
    	index.insert(feature_id, shape.bounds)
    	#creates an index between the feature ID and the bounds of that feature

    print(' - Spatial index created')
    return index

def find_intersection(polygon, index, points):
    intersect_tot=0
    intersect_lon  =[]
    intersect_lat  =[]
    
    for area in polygon:
        shape_geo = shapely.geometry.shape(area['geometry'])
	shape_prep= shapely.prepared.prep(shape_geo)

	for point_id in [int(x) for x in                                       \
                                  list(index.intersection(shb_pol_shy.bounds))]:
	    shape_feature = points[point_id]
	    shape_file    = shapely.geometry(shape_feature['geometry'])
            if shb_pol_pre.contains(shb_pnt_shy): ##NAMING UNCERTAIN
                JS_dom_lon=shb_pnt_fea['properties']['JS_grc_lon']
                JS_dom_lat=shb_pnt_fea['properties']['JS_grc_lat']
                intersect_lon.append(JS_dom_lon)
                intersect_lat.append(JS_dom_lat)
                intersect_tot += 1

    return {'intersect_total':intersect_tot, 'intersect_lon':intersect_lon, 'intersect_lat':intersect_lat }

if __name__ == '__main__':
    check_command_line(sys.argv)

    input_gld_nc4 = sys.argv[1]	##shb_grc_ncf
    input_pol_shp = sys.argv[2] ##shb_fct_ncf
    output_pnt_shp= sys.argv[3] ##shb_pnt_shp
    output_swe_csv= sys.argv[4] ##shb_wsa_csv
    output_swe_ncf= sys.argv[5] ##shb_wsa_ncf


    readFile()
    createShapeFile()

