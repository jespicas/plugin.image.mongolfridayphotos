#!/usr/bin/python

import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
from BeautifulSoup import BeautifulSoup 

import requests


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
print sys.argv
xbmcplugin.setContent(addon_handle, 'movies')
print addon_handle
__settings__   = xbmcaddon.Addon(id="plugin.image.mongolfridayphotos")


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

NumberPagination = 5

r = requests.get('http://www.machacas.com/category/mongol-friday-photos/')
data = r.text
soup = BeautifulSoup(data)
DivPagination = soup.body.findAll("div",{"class": "pagination"})

last = DivPagination[0].findAll('a')

MaxPage = last[len(last)-1].attrs[0][1].split('/')[len(last[len(last)-1].attrs[0][1].split('/')) -1]

def AddItems(Url,currentPage,EndDirectory):
    #print Url
    r = requests.get(Url)
    data = r.text
    soup = BeautifulSoup(data)

    for link in soup.body.findAll("div",{ "class" : "blog-item-wrap" }):
        href = link.find('a').attrs[0][1]
        VolName = href.split('/')[3]
        url = build_url({'mode': 'folder', 'foldername': VolName,'value':href})
        li = xbmcgui.ListItem(VolName, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)

    if (EndDirectory):
        if (currentPage +1) <= MaxPage:
            currentPage = currentPage +1
            NextPage = 'http://www.machacas.com/category/mongol-friday-photos/page/' + str(currentPage)
            url1 = build_url({'mode': 'next', 'foldername': 'Next','value':NextPage})
            li1 = xbmcgui.ListItem('Next' , iconImage='DefaultFolder.png')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url1,listitem=li1, isFolder=True)

        xbmcplugin.endOfDirectory(addon_handle)

def AddImagesInFolder(valors):
    r = requests.get(valors)
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.findAll("img",{"class":"lazy lazy-hidden"}):
        print link.attrs[3][1]
        url = link.attrs[3][1]
        commands = []
        script = ""
        name = "Hello World"
        arg = "ARGS"
        runner = "XBMC.RunScript(" + str(script)+ ", " + str(arg) + ")"
        commands.append(( str(name), runner, ))
        li = xbmcgui.ListItem(url.split('/')[5] + ' Img', iconImage='DefaultVideo.png')
        li.addContextMenuItems( commands )

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    print mode
    xbmcplugin.endOfDirectory(addon_handle)

if mode is None:
    AddItems('http://www.machacas.com/category/mongol-friday-photos/',1,False)
    for Page in range(2,NumberPagination):
        if Page+1 == NumberPagination:
            AddItems('http://www.machacas.com/category/mongol-friday-photos/page/'+str(Page),Page,True)
        else:
            AddItems('http://www.machacas.com/category/mongol-friday-photos/page/'+str(Page),Page,False)


elif mode[0] == 'next':
    print 'Enter on next'
    valors = args['value'][0]
    print valors
    currentPage = int(valors.split('/')[len(valors.split('/'))-1])
    for Page in range(currentPage,currentPage+NumberPagination):
        if (Page +1 == currentPage+NumberPagination):
            AddItems('http://www.machacas.com/category/mongol-friday-photos/page/'+str(Page),int(Page),True)
        else:
            AddItems('http://www.machacas.com/category/mongol-friday-photos/page/'+str(Page),int(Page),False)

elif mode[0] == 'folder':
    foldername = args['foldername'][0]
    print foldername
    valors = args['value'][0]
    print valors
    if __settings__.getSetting("SlideShow") == "true":
        print "SlideShow auto true"
        xbmc.executebuiltin( "SlideShow(plugin://plugin.image.mongolfridayphotos/?foldername="+foldername+"&mode=slideshow&value="+valors+",,notrandom)" )

    AddImagesInFolder(valors)

elif mode[0] == 'slideshow':
    print "SlideShow"
    foldername = args['foldername'][0]
    print foldername
    valors = args['value'][0]
    print valors

    AddImagesInFolder(valors)
