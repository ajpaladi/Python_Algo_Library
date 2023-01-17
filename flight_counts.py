import os
import pandas as pd
import numpy as np
import ipywidgets as widgets
import plotly.express as px
import plotly.graph_objs as go
from tqdm import tqdm_notebook as tqdm
from geolocation_client import ExactEarthClient, XModeClient, WejoClient, ADSBExchangeClient
import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import Point, Polygon
import shapely.wkt
from tqdm import tqdm_notebook as tqdm
import h3
import folium



def flight_counts(report_name, start_date, end_date, airport_geoms, airport_names, save_folder):
    dtype = 'adsb'
    print ('Working with ADS-B')
    provider = ADSBExchangeClient()
    cols = ['flight','r', 't', 'nic', 'rc', 'gs', 'nic_baro', 'nac_p', 'nac_v', 'sil',
            'sil_type','gva', 'sda', 'alt_geom', 'alt_baro', 'emergency', 'alert', 'squawk', 'spi']
    start, end = pd.to_datetime(start_date), pd.to_datetime(end_date)
    start_unix, end_unix = int((start - pd.Timestamp('1970-01-01')) / pd.Timedelta('1s')), int((end - pd.Timestamp('1970-01-01')) / pd.Timedelta('1s'))

    airport_dict = {'date':[], 'airport': [], 'flight_count': [], 'emergency_pings': [], 'emerg_flights': [], 'emerg_squawk':[]}
    emergency_df = pd.DataFrame()
    airport = airport_geoms #input
    airport_name = airport_names #input

    for geom, name in tqdm((zip(airport, airport_name)), total = len(airport)):
    #for item in tqdm((airport), total = len(airport)):
        #for name in airport_name:
        aoi_geom = geom
        aoi_name = name
        pings = provider.get_pings_in_area(aoi_geom.wkt, start_unix, end_unix, columns=cols, gh_filter_precision=5)
        pings['unixtime'] = pd.to_datetime(pings['unixtime'], unit ='s')
        pings['date'] = pings['unixtime'].dt.strftime('%Y-%m-%d')
        pings['date'] = pd.to_datetime(pings['date'])
        pings = pings[(pings.t != '') + (pings.emergency != '')]
        pings['airport'] = aoi_name
        emergency_app = pings[(pings.emergency != 'none') & (pings.emergency != '')]
        emergency_df = emergency_df.append(emergency_app)
        for date in tqdm((pings.date.unique()), total = len(pings.date.unique())):
            df = pings[(pings.date == date)] 
            emergency = df[(df.emergency != 'none') & (df.emergency != '')]
            emergency = emergency[(emergency['flight'] != '')]
            emerg_fligts = emergency.flight.unique()  #going to be an array
            emerg_squawk = emergency.squawk.unique()  #going to be an array
            airport_dict['emerg_flights'].append(emerg_fligts)
            airport_dict['emerg_squawk'].append(emerg_squawk) 
            emergency_count = emergency['emergency'].count()
            airport_dict['emergency_pings'].append(emergency_count)
            airport_dict['airport'].append(df['airport'].unique()) ##this was changed
            date_unique = df.date.unique()
            airport_dict['date'].append(date_unique)
            ping_filter = df[(df.gs < 50)]
            ping_filter.drop_duplicates(subset = 'flight', inplace = True)
            flight_count = len(ping_filter.flight.unique())
            airport_dict['flight_count'].append(flight_count) #dict append

    report = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in airport_dict.items() ]))
    report['date'] = report['date'].str[0]
    report['date'] = pd.to_datetime(report['date'], format = '%Y-%m-%d')
    report['airport'] = report['airport'].str[0]
    report['emerg_flights'] = report['emerg_flights'].str[0]
    report['emerg_squawk'] = report['emerg_squawk'].str[0]
    report = report.fillna(0)
    report.to_csv(save_folder + '/' + report_name + '.csv')
    print("script completed, report saved")
    return flight_counts

###example

'''
atl = shapely.wkt.loads('MultiPolygon (((-84.4577496211375518 33.63325886013930699, -84.45797949324744991 33.63469937885763272, -84.45749364987138108 33.63779011549392095, -84.4560764952169194 33.64057944685220747, -84.45386675025554268 33.64279433374472461, -84.45108072022027557 33.64421796761040895, -84.4479911211423655 33.6447109932474504, -84.44787382276594201 33.64471112956165655, -84.44796672096954637 33.64530024168520583, -84.44856136224012744 33.64647711405790176, -84.44904034280453686 33.64956892167802494, -84.44854045929353958 33.65265741859666093, -84.4471106437880934 33.6554402812165776, -84.44489085659196803 33.657645103555204, -84.44209838594210282 33.65905606224012558, -84.43900657832196543 33.65953504280454212, -84.43884939161524983 33.65953451116968154, -84.43690140501838926 33.65953579781869109, -84.43031993356289888 33.65954009786563006, -84.42754857394039902 33.65954189732005375, -84.42488435484690967 33.6595440965928745, -84.42399588199282334 33.65954479689371226, -84.422873250798105 33.65954499938214184, -84.42171881443219661 33.6595457976095318, -84.41911345995289651 33.65954749784840061, -84.41850679304297955 33.65954789782659162, -84.41773407165278797 33.65954839790588693, -84.41114068506064427 33.65954830038504753, -84.4101843210222853 33.65955317035163574, -84.41001485468495957 33.65955259732572813, -84.40953181776643532 33.65954687074696494, -84.40938918186282081 33.65954583777723741, -84.40630263734627192 33.65903403733918964, -84.40352531410407266 33.65759349148804347, -84.40206925359301238 33.65611618754095247, -84.39975292540307805 33.65497607773666999, -84.39751018884847156 33.65279460358197383, -84.39605133222048039 33.65002685466274102, -84.39551915857029485 33.64694375752722522, -84.39596576076264967 33.64384710720425886, -84.39734742226333708 33.64104002540307903, -84.39869823233388502 33.63965128049540709, -84.39775240213518259 33.63778956719522029, -84.39726660693490601 33.63469882298640101, -84.39775968072987666 33.63160923159372828, -84.39918335802161664 33.62882322374916555, -84.40139827935745132 33.6266135133117956, -84.40418763280477776 33.62519640213518812, -84.40727837701359704 33.62471060693490443, -84.4080277887482282 33.62471148951873801, -84.40890161877194942 33.62470993414211762, -84.40904773711093867 33.62470937358583001, -84.40911169948498127 33.62470933276673435, -84.40949254432420901 33.62471030771310154, -84.40879786121534778 33.62333154060018359, -84.40832240220008487 33.62023918947753032, -84.40882580285487791 33.61715126387581876, -84.41025878681621464 33.61437003146777869, -84.41248108362978542 33.61216773865950813, -84.41527515939981186 33.61075996121534359, -84.41836751052247223 33.61028450220009489, -84.41894823070040843 33.61028712769319071, -84.42039013703872286 33.61028889413395149, -84.42695772335318338 33.61028260458561334, -84.4342242450653373 33.61028060037948251, -84.43477465341200627 33.61028050027952929, -84.43900122467840674 33.6102792004728812, -84.44589239081538778 33.61028169915665842, -84.44717139133669548 33.61028110473348818, -84.44780173025220904 33.61027982074634934, -84.45089289075140471 33.61076295996976171, -84.45368346085638223 33.61217767380306043, -84.45590028012225048 33.61438548019933847, -84.45732635083375328 33.61717026368585692, -84.4578220792536456 33.62025943025221153, -84.45733894003022613 33.62335059075140009, -84.45602217078314311 33.62594796190141722, -84.45615701498212502 33.62608727114010776, -84.45753182587939989 33.62889771447483156, -84.45797087398976544 33.63199544485330961, -84.4577496211375518 33.63325886013930699)))')
save_folder = '/Users/andrewpaladino/Documents/local_notebooks'
flight_counts('atl', '2023-01-08', '2023-01-09', [atl], ['atl'], save_folder)
'''
 
