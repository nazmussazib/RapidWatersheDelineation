__author__ = 'shams'

from Rapid_Watershed_Delineation import *


##big area : -75.215759,40.018540
##coasta area: -74.500752  39.340927
##coastal area : -74.467992  39.343667
## at corner -74.499520  39.332364
##near river -74.922294  40.063649
##inside a island -74.168243  39.695785
##in ocean and steam -74.159819  39.688902
latitude= -74.159819  ## user input latitude from clicking on the map
longitude=39.688902 ## user input longitude from clicking on the map
snapping=1  ##user input snapping option ( on=1,off=0)
maximum_snap_distance=10000 ##user input maximum snapping distance


""" One time input from Pre-Processing Product"""

Pre_process_TauDEM_dir='F:\USU_Research_work_update_March_30_2014\MMW_PROJECT\OnFlyWatershed_GEO_Delaware'
gage_watershed_file="delaware_gw_5000_diss"
elev_file='DelDEMGeo2fel.tif'
max_elev_file='DelDEMGeo2Max_elv_upslope.tif'
Ad8_weighted_file='DelDEMGeo2ad8_slope_weighted.tif'
Ad8_file='DelDEMGeo2ad8.tif'
gord_file='DelDEMGeo2gord_peuker.tif'
plen_file='DelDEMGeo2plen.tif'
tlen_file='DelDEMGeo2tlen.tif'
coast_watershed_file='Delaware_Missing_Coast_Watershed'
Ocean_stream_file='Delaware_Ocean_stream_dissolve'
np=8
TauDEM_dir='E:\\USU_Research_work\\MMW_PROJECT\\TauDEM_Project\\TauDEM_deploy_6_working_copy\\Taudem5PCVS2010\\x64\\Release'
MPI_dir='C:\\Program Files\\Microsoft HPC Pack 2012\\Bin'


##run Point Watershed Function
Point_Watershed_Function(latitude,longitude,snapping,maximum_snap_distance,Pre_process_TauDEM_dir,
Ocean_stream_file,gage_watershed_file,coast_watershed_file,elev_file,max_elev_file,Ad8_weighted_file,Ad8_file,plen_file,tlen_file,gord_file,np,TauDEM_dir, MPI_dir)



