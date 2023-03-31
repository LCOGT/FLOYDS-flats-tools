#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:02:53 2023

@author: pkottapalli
"""

"""
Get all unique alt az data. Including red and blue lampflats,
red and blue science frames
all rectified, flat corrected,
and also raw
"""
#%% Imports
import requests
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from urllib.parse import urljoin
import os
#%% Authenticate
requests.post(
    'https://observe.lco.global/api/api-token-auth/',
    data = {
        'username': 'eng@lco.global',
        'password': 'sbatoo1'
    }
).json()
#%%
import csv
csv_path = '/home/pkottapalli/Downloads/On_demand_report_2023-03-16T17 02 56.539Z_65dbdeb0-c41c-11ed-8948-cb80406fa13a.csv'
filenames = []
with open(csv_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        filename = row[0]
        filenames.append(filename)
#filenames=sorted(filenames)
#%%
#Get all headers from a year
altitude = []
azimuth = []
rotangle = []
frameid = []
for f in filenames[1:]:
    filename = os.path.splitext(os.path.splitext(f)[0])[0]
    print(filename)
    archive_record = requests.get(f'https://archive-api.lco.global/frames/?site_id=ogg&basename={filename}&start=2022-01-01 00%3A00&end=2023-01-01 00%3A00&public=true&limit=1000', headers={'Authorization': 'Token efc8c22ed48db4962008085fc4af4bfa5354fd7d'}).json()
    if len(archive_record['results']) > 0:
        rec = archive_record['results'][0]
        frame_id = rec["id"]
        frameid.append(frame_id)
        header = requests.get(f'https://archive-api.lco.global/frames/{frame_id}/headers/', headers={'Authorization': 'Token efc8c22ed48db4962008085fc4af4bfa5354fd7d'}).json()
        altitude.append(header['data']['ALTITUDE'])
        azimuth.append(header['data']['AZIMUTH'])
        rotangle.append(header['data']['ROTANGLE'])
    else:
        print('could not find ' + filename)
df = pd.DataFrame({'Altitude':altitude, 'Azimuth':azimuth, 'Rotangle': rotangle}, index=frameid)
#%% Plot the locations of each coordinate
plt.figure(dpi=200)
plt.scatter(altitude, azimuth, s=2, alpha = 0.3)
plt.xlabel('Altitude')
plt.ylabel('Azimuth')
plt.show()
#%% Find observations that were close to each other in the alt-rot space
#Take a circular approximation for the distance between points in alt-rot space
unique_coords = []
for i in range(len(altitude)):
    for k in range(len(altitude)):
        dist = (altitude[i]-altitude[k])**2 + (rotangle[i]-rotangle[k])**2
    if dist > 1:
        unique_coords.append(df.index[i])
#%% download the frames that are unique
import multiprocessing

doubles_path = 'All_AltAz_data'
def download_file(records):
    for frame_id in records:
        print(frame_id)
        archive_record = requests.get(f'https://archive-api.lco.global/frames/?instrument_id=en06&site_id=ogg&start=2022-01-01&end=2023-01-01&configuration_type=LAMPFLAT&id{frame_id}&public=true&limit=1000', headers={'Authorization': 'Token efc8c22ed48db4962008085fc4af4bfa5354fd7d'}).json()['results']
        for rec in archive_record:
            #Give path to write files to
            with open(f'{doubles_path}/{rec["filename"]}', 'wb') as f:
                f.write(requests.get(rec['url']).content)
            
N_PROCESSES = multiprocessing.cpu_count()
with multiprocessing.Pool(N_PROCESSES) as pool:
    pool.map(download_file, unique_coords)
    pool.close()
    pool.join()
    
#%%
download_file(unique_coords)