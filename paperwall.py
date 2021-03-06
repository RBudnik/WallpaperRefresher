from urllib  import request
from bs4     import BeautifulSoup
from general import *

def getLink(s):
    ''' (string) -> string
    Cuts necessary link from part of the html page.
    '''
    if s[1]=='i':
        begin = s.find('wallp')
        end = max(s.find('jpg'), s.find('png'))+3
        link = s[begin:end]
    elif s[1]=='d':
        begin = s.find('wallp')
        end = s.find('" ',begin)
        link = s[begin:end]
    result = 'http://thepaperwall.com/' + link
    return result

def getWOTD():
    ''' 
    Finds and downloads Wallpaper of the Day at paperwall.com for further use.
    '''
    print(' > | Getting you Wallpaper of the day from Paperwall...')
    page = request.urlopen('http://thepaperwall.com/index.php')
    soup = BeautifulSoup(page)
    block = str(soup.find('div',class_='active'))
    link = getLink(block)

    page = request.urlopen(link)
    soup = BeautifulSoup(page)
    block = str(soup.find('img',class_='wall_img'))
    link = getLink(block)
    getImage(link)
    setwp(imgpath)

def getTagged(tag):
    ''' (string)
    Finds, downloads and sets up wallpaper with specified tag.
    '''    
    print(' > | You are looking for wallpaper tagged: '+tag)
    tag = tag.replace(' ','+')
    tag = tag[:len(tag)-1]
    page = request.urlopen('http://thepaperwall.com/search.php?search='+tag)
    soup = BeautifulSoup(page)
    group = soup.find_all('div',class_='single_thumbnail_cont')

    # First filter: resolution
    for s in group:
        sstr = str(s)
        begin = sstr.find('<span>')+6
        end = sstr.find('</span>')
        resol = sstr[begin:end].split()
        resol.remove('x')
        if int(resol[0])<width or int(resol[1])<height:
            group.remove(s)

    # Second filter: clean links
    for s in group:
        group[group.index(s)] = getLink(str(s))

    n = 0
    while True:
        try: page = request.urlopen(group[n])
        except IndexError:
            if n>0:
                print(' ! | I got nothing more :( ')
                break
            else:
                print(' ! | I found nothing :( ')
                break
        soup = BeautifulSoup(page)
        block = str(soup.find('img',class_='wall_img'))
        link = getLink(block)
        getImage(link)
        setwp(imgpath)
        break
        if input(' ? | You happy now? (y/n) ')=='y': break
        else: n+=1
