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

def check_command_line_arg():
    ##Checks the length of arguements and if input files exist
    IS_arg = len(sys.argv)
    if IS_arg != 6:
        print('ERROR - 5 and only 5 arguments can be used')
        raise SystemExit(22) 

    for shb_file in sys.argv[2:5]:
	try:
            with open(shb_file) as file:
	        pass
	except IOError as e:
            print('ERROR - Unable to open ' + shb_file)
            raise SystemExit(22) 
    
    print('[+] Command Line Entered Properly')


def readFile(gld_ncf):##Currently Can Delete
    dimensions = dict()
    print('Read GLD netCDF file')

    #Open netCDF file
    f = netCDF4.Dataset(gld_ncf, 'r')
    
    #Get Dimension Sizes
    gld_lon = len(f.dimensions['lon'])
    print(' - The number of longitudes is: '+str(IS_grc_lon))
    
    gld_lat = len(f.dimensions['lat'])
    print(' - The number of latitudes is: '+str(IS_grc_lat))
    
    gld_time= len(f.dimensions['time'])
    print(' - The number of time steps is: '+str(IS_grc_time))

    return dimensions


def readPolygonShpFile(polyFile):
    print('Read polygon shapefile')
    polygon_file = fiona.open(polyFile, 'r')
    polygon_features=(polygon_file)
    print(' - The number of polygone features is: ' + str(polygon_features))
    return polygon_file

def createShapeFile(gld_dim_lat_length, gld_dim_lon_length, lon_dimension_array, gld_lat_length_dimension_array, polygonShapeFile):
    shapeFile_Driver= polygonShapeFile.driver
    shapeFile_Point = shapeFile_Driver
    
    shapeFile_crs = polygonShapeFile.crs
    shapeFilePoint_crs   = shapeFile_crs.copy()

	##Kept the same names, just in case
    shapeFile_schema= {'geometry':'Point',
			'properties':{
					'JS_gld_lon': 'int:4',	\
					'JS_gld_lat': 'int:4'}}

 
    with fiona.open(output_pnt_shp, 'w', driver=shapeFile_Point, \
			crs=shapeFilePoint_crs,
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
				
    print('[+] New ShapeFile Created')


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

    return (intersect_tot, intersect_lon, intersect_lat)

if __name__ == '__main__':
    check_command_line_arg()

    input_gld_nc4 = sys.argv[1]	##shb_grc_ncf
    input_pol_shp = sys.argv[2] ##shb_pol_ncf
    output_pnt_shp= sys.argv[3] ##shb_pnt_shp
    output_swe_csv= sys.argv[4] ##shb_wsa_csv
    output_swe_ncf= sys.argv[5] ##shb_wsa_ncf

    print('Read GLD netCDF file')
    f = netCDF4.Dataset(input_gld_nc4, 'r')
    #Dimension Sizes
    number_of_lon=len(f.dimensions['lon'])		##IS_grc_lon
    number_of_lat=len(f.dimensions['lat'])		##IS_grc_lat
    num_of_time_steps=len(f.dimensions['time'])		##IS_grc_time

    #Value of Dimension Arrays
    gld_lon =f.variables['lon']		##ZV_grc_lon
    gld_lat =f.variables['lat']		##ZV_grc_lat
    gld_time=f.variables['time']	##ZV_grc_time

    #Get Interval Sizes
    gld_lon_interval_size =abs(gld_lon[1]-gld_lon[0])
    gld_lat_interval_size =abs(gld_lat[1]-gld_lat[0])
    if len(gld_time) < 1:
	gld_time_interval_size=abs(gld_time[1]-gld_time[0])
    else:
	gld_time_interbal_Size=0

    #Get Fill Values
    gld_fill = netCDF4.default.fillvals['f4']
    if 'RUNSF' in f.variables:
	gld_fill = var._FillValue
	print(' - The fill value for RUNSF is: '+str(ZS_grc_fil))
    else:
	gld_fill = None

    print('[+] Variables are set up properly')		##Can Delete



    polyShapeFile = readPolygonShpFile(input_pol_shp)	##shb_pol_lay
    #createShapeFile(gld_dim_lat_length, gld_dim_lon_length, lon_dimension_array, gld_lat_length_dimension_array, polygonShapeFile)

    #point_features=fiona.open(shb_pnt_shp, 'r')		##shb_pnt_lay
    #index = createSpatialIndex(point_features)
    #find_intersection(output_pnt_shp, index, point_features)





    print('[+] Script Completed')
