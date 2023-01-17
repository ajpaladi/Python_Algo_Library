import pandas as pd
import geopandas as geo
import os
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.point import Point

def get_ports(project_name, pings, tracks, call_sign, output_folder):
    geolocation_pings = pd.read_csv(pings)
    emr_tracks = pd.read_csv(tracks)
    call_sign = pd.read_csv(call_sign)
    geolocation_pings.rename(columns = {'device_id':'mmsi'}, inplace = True)
    geolocation_pings = geolocation_pings[['mmsi', 'vessel_type_code', 'vessel_name', 'callsign']]
    geolocation_pings = geolocation_pings.drop_duplicates()
    results = geolocation_pings.merge(emr_tracks, on='mmsi') #how='right')
    update = call_sign['Series'].str[:-7]
    call_sign['Series'] = update
    call_sign = call_sign.rename(columns = {'Allocated to':'Country'})
    results['callsign_new'] = results['callsign']
    update_column = results['callsign_new'].str[0:2]
    results['callsign_new'] = update_column
    results = results.rename(columns = {'callsign_new':'Series'})
    final = call_sign.merge(results, on='Series')
    ports = final[(final.nav_status == "Moored") & (final.sog == 0)]
    ports.to_csv(output_folder + project_name + '.csv') #to save to CSV
    print('Completed, output saved')
    return get_ports
    

'''  
Example:

project_name = 'Sabine'
geolocation_pings = '/Users/andrewpaladino/Documents/projects/Ankura/ais/pings.csv'
emr_tracks = '/Users/andrewpaladino/Documents/projects/Ankura/ais/tracks.csv'
call_sign = '/Users/andrewpaladino/Documents/projects/Cheniere/article_II/inputs/call_sign.csv'
output_folder = '/Users/andrewpaladino/Documents/local_notebooks/'

get_ports(project_name, geolocation_pings, emr_tracks, call_sign, output_folder)
'''
