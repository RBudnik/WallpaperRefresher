from urllib  import request
from urllib  import parse
from bs4     import BeautifulSoup
from ctypes  import *
from general import *
import os,time,sys,base64

def needwp(img):
    ''' (string) -> boolean
    Checks if wallpaper image needs update by watching date of bmp modification
    '''
    modified = time.ctime(os.stat(img).st_mtime)
    modified = modified.split()
    modified = modified[2]
    print(' > | Wp modified: '+modified)
    today = time.strftime('%d')
    if modified!=today:
        print(' ! | Wallpaper needs update!')
        getWOTD()
        setwp(img)
    else:
        print(' + | Wallpaper is up to date.')

def getLink(s):
    ''' (string) -> string
    Cuts necessary link from part of the html page.
    '''
    result = 'None'
    if s[1]=='s':
        begin = s.find('+B')+4
        end = s.find(')+')-1
        result = str(base64.b64decode(s[begin:end]),encoding='UTF-8')
    elif s[1]=='d':
        begin = s.find('id="thumb')+9
        end = s.find('" ',begin)
        link = s[begin:end]
        result = 'http://wallbase.cc/wallpaper/' + link
    return result

def getWOTD():
    ''' 
    Finds and downloads Wallpaper of the Day at paperwall.com for further use.
    '''
    print(' > | Getting you Wallpaper of the day...')
    page = request.urlopen('http://wallbase.cc/toplist/0/12/gteq/'+str(width)+'x'+str(height)+'/0/100/32/1d')
    soup = BeautifulSoup(page)
    block = str(soup.find('div',class_='thumb'))
    link = getLink(block)

    page = request.urlopen(link)
    soup = BeautifulSoup(page)
    soup = soup.find_all('div',class_='right')
    block = str(soup[len(soup)-1])
    link = getLink(block[33:])
    getImage(link)

def getTagged(tag):
    ''' (string)
    Finds, downloads and sets up wallpaper with specified tag.
    '''    
    print(' > | You are looking for wallpaper tagged:',tag)
    params = {
      'query' : tag,
      'board' : 213,    # ???
      'nsfw' : 100,     # Bit-mask: sfw-sketchy-nsfw
      'res' : str(width)+'x'+str(height), # Resolution
      'res_opt' : 'qteq',   # qteq - "at least" resolution
      'aspect' : 0,     
      'orderby' : 'random', # Change to 'random' if not testing
      'orderby_opt' : 'desc',
      'thpp' : 60,      # ???
      'section' : 'wallpapers' # ???
    }
    params = parse.urlencode(params)
    params = params.encode('utf-8')
    page = request.urlopen('http://wallbase.cc/search',params)
    soup = BeautifulSoup(page)
    group = soup.find_all('div',class_='thumb')
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
        soup = soup.find_all('div',class_='right')
        block = str(soup[len(soup)-1])
        link = getLink(block[33:])
        getImage(link)
        setwp(imgpath)
        if input(' ? | You happy now? (y/n) ')=='y': break
        else: n+=1