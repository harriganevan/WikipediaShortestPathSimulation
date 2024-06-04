import json
import time
import requests
from collections import deque

#create a function that returns shortest route given start and end page

def getLinks(title):
    links = []

    response = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=links&titles={}&pllimit=500&format=json&redirects=true'.format(title))
    wikiLinks = response.json()

    pageId = next(iter(wikiLinks['query']['pages']))

    for link in wikiLinks['query']['pages'][pageId]['links']:
        if link['ns'] == 0:
            links.append(link['title']) 

    continuedLinks = wikiLinks

    while 'continue' in continuedLinks:
        response = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=links&titles={}&pllimit=500&format=json&plcontinue={}&redirects=true'.format(title, continuedLinks['continue']['plcontinue']))
        wikiLinks = response.json()

        for link in wikiLinks['query']['pages'][pageId]['links']:
            if link['ns'] == 0:
                links.append(link['title'])

        continuedLinks = wikiLinks

    return links

def checkPages(start, stop):
    for title in [start, stop]:
        try:
            result = requests.get('https://en.wikipedia.org/wiki/'+title)
            if result.status_code == 404:
                print(title+' is not a valid Wikipedia page')
                return False
        except:
            print(title+' is not a valid Wikipedia page')
            return False

    #check for dead end start page
    if len(getLinks(start)) == 0:
        print('Start page is a dead-end; There are no links on this page')
        return False

    #check for orphan end page

    return True

def getRoute(start, stop):
    if checkPages(start, stop) :
        print('getting route for '+start+' -> '+stop)