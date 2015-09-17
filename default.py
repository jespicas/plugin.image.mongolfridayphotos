#!/usr/bin/python

import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
from BeautifulSoup import BeautifulSoup 

import requests


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    r = requests.get('http://www.machacas.com/category/mongol-friday-photos/')
    data = r.text
    soup = BeautifulSoup(data)

    for link in soup.body.findAll("div",{ "class" : "blog-item-wrap" }):
        href = link.find('a').attrs[0][1]
        VolName = href.split('/')[3]
        url = build_url({'mode': 'folder', 'foldername': VolName,'value':href})
        li = xbmcgui.ListItem(VolName, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)

    NextPage = 'http://www.machacas.com/category/mongol-friday-photos/page/2'
    url1 = build_url({'mode': 'next', 'foldername': 'Next','value':NextPage})
    li1 = xbmcgui.ListItem('Next' , iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url1,listitem=li1, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'next':
    print 'Enter on next'
    valors = args['value'][0]
    print valors

    r = requests.get(valors)
    data = r.text
    soup = BeautifulSoup(data)

    for link in soup.body.findAll("div",{ "class" : "blog-item-wrap" }):
        href = link.find('a').attrs[0][1]
        print href
        VolName = href.split('/')[3]
        print VolName
        url = build_url({'mode': 'folder', 'foldername': VolName,'value':href})
        li = xbmcgui.ListItem(VolName, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)

    NextPage = 'http://www.machacas.com/category/mongol-friday-photos/page/3'
    url1 = build_url({'mode': 'next', 'foldername': 'Next','value':NextPage})
    li1 = xbmcgui.ListItem('Next' , iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url1,listitem=li1, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'folder':
    foldername = args['foldername'][0]
    print foldername
    valors = args['value'][0]
    print valors
    #url = 'https://googledrive.com/host/0B2XIl3N1QXfyc1lETGRFNjhubm8/01.jpg'
    #li = xbmcgui.ListItem(foldername + ' Video', iconImage='DefaultVideo.png')
    #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    #xbmcplugin.endOfDirectory(addon_handle)
    r = requests.get(valors)
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.findAll("img",{"class":"lazy lazy-hidden"}):
        print link.attrs[3][1]
        url = link.attrs[3][1]
        li = xbmcgui.ListItem(url.split('/')[4] + ' Img', iconImage='DefaultVideo.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    
    xbmcplugin.endOfDirectory(addon_handle)
    #dialog = xbmcgui.Dialog()
    #dialog.notification('Movie Trailers', valors, xbmcgui.NOTIFICATION_INFO, 5000)

    #d = requests.get(valors)
    #datas = d.text
    #soup = BeautifulSoup(datas)
    #print soup.body.find("img",{"class":"lazy"})
    #for link in soup.body.findAll("img",{ "class" : "lazy" }):
    #	url = link.attrs[3]
    #	print url
    #	li = xbmcgui.ListItem(foldername + ' Img', iconImage='DefaultVideo.png')
    #	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    #	xbmcplugin.endOfDirectory(addon_handle)
