import json
import time
import requests
from collections import deque
from random import shuffle

def findShortestPath(start, end):
    path = {}
    path[start] = [start]
    queue = deque([start])

    while len(queue) != 0:
        page = queue.popleft()
        links = getLinks(page)

        for link in links:
            if link.lower() == end.lower():
                return path[page] + [link]
            if (link not in path) and (link != page):
                path[link] = path[page] + [link]
                queue.append(link)

    return None

#return true if title has a backlink; false otherwise 
def hasBacklinks(title):
    response = requests.get('https://en.wikipedia.org/w/api.php?action=query&list=backlinks&bltitle={}&blnamespace=0&format=json&blredirect=true'.format(title))
    wikiLinks = response.json()
    return len(wikiLinks['query']['backlinks']) > 0

#return array of links on title page
def getLinks(title):

    print(title)

    links = []

    response = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=links&titles={}&pllimit=500&format=json&redirects=true'.format(title))
    wikiLinks = response.json()

    pageId = next(iter(wikiLinks['query']['pages']))

    if pageId != '-1':

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

    shuffle(links)
    return links

#checks validity of start and end page
def checkPages(start, end):

    #check start and end pages exists
    for title in [start, end]:
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
    if not hasBacklinks(end):
        print('End page is an orphan; no other pages can get to it')
        return False

    return True

def getRoute(start, end):

    #check if pages are valid
    if checkPages(start, end) :
        starttime = time.time()
        print('finding shortest route for '+start+' -> '+end+'...')
        route = findShortestPath(start, end)
        endtime= time.time()
        totaltime = endtime - starttime
        print('Time: {}m {:.3f}s'.format(int(totaltime)//60, totaltime%60))

        return route
