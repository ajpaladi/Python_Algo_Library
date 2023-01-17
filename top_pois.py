import pandas as pd
import geopandas as geo
import numpy as np
import os
import ipywidgets as widgets
import plotly.express as px
import plotly.graph_objs as go
import go_utils
from go_utils import GoProject
from go_utils import GoResults
from go_utils import GoResultsTraceability
import uuid
import osmnx as ox
from shapely.geometry import Polygon
from geopy.geocoders import Nominatim
locator = Nominatim(user_agent="myGeocoder")
go_utils.OI_TOKEN = os.environ['GO_API_TOKEN']

def top_pois(project_id, quantile, file_name):
    project_id = project_id
    project = GoProject(project_id)
    results = project.get_traceability_results()  #this will pull everything
    clusters = results.get_all_clusters()
    heatmap = results.get_all_heatmaps()
    
    crs = {'init': 'epsg:4326'}
    heatmap_gdf = geo.GeoDataFrame(heatmap, crs=crs, geometry=heatmap['geometry'])
    heatmap_sorted = heatmap.sort_values(by = 'total_trips', ascending = False)
    quantile_90_trips = heatmap_sorted['total_trips'].quantile(q = quantile)
    quantile_90_devices = heatmap_sorted['total_devices'].quantile(q = quantile)
    heatmap_prod = heatmap_sorted[(heatmap_sorted.total_trips > quantile_90_trips)]
    heatmap_prod['unique_id'] = heatmap_prod['total_trips'].rank(ascending=False)
    
    bounds = heatmap_prod.total_bounds
    tags = {"building": True}
    north = bounds[1] #latitude
    south = bounds[3] #latitude
    east = bounds[0]  #longitude
    west = bounds[2]  #longitude

    #rather than do a bounding box, it might be good to dissovle geometries of the heatmap and do it that way?
    osm_pull = ox.geometries.geometries_from_bbox(north, south, east, west, tags)#this will take AWHILE depending on the size of your bounding box
    buildings = ox.project_gdf(osm_pull)
    buildings.drop(columns = 'unique_id')
    
    buildings = buildings.to_crs({'init': 'epsg:4326'})
    heatmap_prod = heatmap_prod.to_crs({'init': 'epsg:4326'})
    
    merge = geo.sjoin(heatmap_prod, buildings, how = 'inner', op = 'intersects')
    export = test[['unique_id_left','total_trips', 'total_devices', 'addr:city', 'addr:street', 'shop', 'name', 'geometry']]
    production = export.dropna(axis = 0, subset = ['name'])
    
    production.sort_values(by = 'total_trips', ascending = False)
    production['centroid'] = production['geometry'].centroid
    production.rename(columns = {'unique_id_left':'grid_id'}, inplace = True)
    
    production['lon'] = production.centroid.apply(lambda p: p.x)
    production['lat'] = production.centroid.apply(lambda p: p.y)
    production['tuple'] = production.apply(lambda row: (str(row.lat),str(row.lon)),axis=1)
    production['address'] = production.apply(lambda row: locator.reverse(row.tuple).address,axis=1)
    
    production.to_csv(file_name + '.csv')
    
    #maybe I should have returned the production df rather than the function
    return top_pois 
