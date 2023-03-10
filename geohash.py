import os
import datetime
import pandas as pd
import geopandas as gpd
import plotly.express as px
import shapely.wkt 
from shapely.geometry import Point, Polygon, MultiPolygon
from polygon_geohasher import polygon_geohasher as pg

#input must be wkt
def geom_to_geohash(aoi_name, aoi_geometry):
    geohashes = (polygon_to_geohashes(aoi_geometry, 7))
    df = pd.DataFrame(geohashes)
    df['name'] = aoi_name
    df.rename(columns = {0:'geohash'}, inplace = True)
    df.rename(columns = {'name':'aoi_name'}, inplace = True)
    df.to_csv('{}_geohash.csv'.format(aoi_name))
    return geohash

def geohash_to_geom(csv):
    aois = pd.read_csv(csv)
    aois = aois.groupby(by='aoi_name').agg({'geohash':list}).reset_index()
    aois['geometry'] = aois['geohash'].apply(pg.geohashes_to_polygon)
    geom = gpd.GeoDataFrame(aois, geometry='geometry', crs='EPSG:4326')
    geom.rename(columns = {'aoi_name': 'name'}, inplace = True)
    geom.to_csv('geometries.csv')
    return geom

### examples ###

#example of input aoi_geom
#ankura = shapely.wkt.loads('MultiPolygon (((37.08932387968397393 56.78629694854799936, 37.26125409376248854 56.79993390637520179, 37.26907988281695339 56.75120771120606378, 37.11185266635592939 56.72636551192442766, 37.0969125236155719 56.75250789755278902, 37.08932387968397393 56.78629694854799936)))')
#geohash_to_geom('aois_gh7.csv')
