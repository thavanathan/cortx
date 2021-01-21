#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################################
# Author		: Venkatesh K
# Date			: 20-01-2021
# Description		: Used to get total user count  from slack
# Usage			: python file_name.py
#######################################################################
import re
import requests
import json
import os
import sys
import html
#from dateutil import parser
import datetime

# todo 
# change the token into env variable
token = 'xoxs-1159580943030-1213988393956-1655315023763-378950a18d12809e302e66d867d5800b186fb5912a3d9df541153e51dde6611d'
url = 'https://cortxcommunity.slack.com/api/team.stats.export'

payload = {'token':token,'offline':'false'}

def clean(data):
    """ Clean the html tags and remove un-wanted white space
    Parameters
    ----------
    Data: 
       Raw html data with tags & multiple whitespaces
    Returns:
       Remove spaces, taggs and return the enriched data
    """
    data = str(data)
    data = data.replace(',', '')
    data = re.sub('\s+', ' ', data)
    data = re.sub('<[^>]*?>', '', data)
    data = data.strip()
    return data

def api_process(url):
    """ Process the slack url to get user count
    If the argument isn't passed in, the function throw an error.
    Parameters
    ----------
    Url : str, require
	The url for minio, ceph and daos
    Returns:
        The user count of given url.
    """
    try:
        response = requests.get(url)
        data = html.unescape(response.text)
        count_obj = re.search(r'\"total\">(\d+)<\/b>\s*users', data)
        total_count = clean(count_obj.group(1))
    except:
       pass
       #todo
    return total_count

def download_csv(type, date_range):
    """ Download the csv file for the given type and save it.
    Parameters:
    ----------
    Type: overview, channels, users
       Date Range: 30d, 15d, 1d

    Returns:
       None.
    """
    print('Beginning %s file download with requests' %(type))
    try:
       payload.update({'type': type, 'date_range': date_range})
       response = requests.get(url, params=payload)
       filename = type + '.csv'
       with open(filename, 'wb') as f:
          f.write(response.content)
    except:
       pass
       # todo
    return


"""
def export_csv(login_url, download_url, user, password):
    #response = requests.get(url, auth=(user, password))
    session = requests.Session()
    session.get(login_url)
    session.post(login_url, data={'_username': user, '_password': password})
    res = session.get(download_url)
    with open ("output.csv", "w") as fobj:
        fobj.write (res.text)
"""
        
def main():
    result = api_process("https://slack.openio.io/")
    print ("Minio total count %s" %(result))
    result = api_process("http://slackin-ceph-public.herokuapp.com/")
    print ("Ceph total count %s" %(result))
   
    #todo
    download_csv('overview', '30d')
    download_csv('users', '30d')
    download_csv('channels', '30d')


if __name__ == '__main__':
  main()

