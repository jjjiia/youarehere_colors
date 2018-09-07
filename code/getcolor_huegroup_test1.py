from __future__ import with_statement

import os
import os.path
import Image
import math
import csv
import sys
#FUNCTION FOR CONVERTING RGB TO HSV
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h,s,v

#MAKE LIST OF FILES IN A DIRECTORY
folderNumber = 0
for folderNumber in range(0, 42):
    print folderNumber
    for path, subirs, files in os.walk(r'/Users/jiazhang/Documents/GitHub/streetview_downloader/cambridge-split/images-'+str(folderNumber)):
        currentdir = []
        files = [f for f in files if not f[0] == '.']
        for filename in files:
            #JOIN NAME WITH PATH
            f = os.path.join(path, filename)
            currentdir.append(f)       
       # print currentdir
    folderNumber = folderNumber+1
    values = []
    #MAKE DICTIONARY
    #make hue dictionary

    #OPEN FILES IN LIST AND GET COLOR
    #  hues grouped into 6 degrees each
    basepath = '/Users/jiazhang/Documents/GitHub/streetviewcolor/'
    with open(basepath+'cambridge_huegroups'+str(folderNumber)+'.csv', 'w') as csvfile:
      
        spamwriter = csv.writer(csvfile)
        print "open"
        for file in currentdir:
            huefreq={}
            huegroup = 0
            for huegroup in range(0,60):
                huefreq[huegroup]=0
            #print "reset",huefreq
            
            #print file
            image = Image.open(file)
            width, height = image.size
            imgstat = os.stat(file)
            pix = image.load()
            #print imgstat
            #print imgstat[6]
            #CHECK IF IMAGE IS BLANK, AND REMOVE
            if imgstat[6] < 4483:
                os.remove(file)
            for x in range(0,width):
                for y in range(0,height):
                    r,g,b = pix[x,y]
                    rgb = (r,g,b)
                    hexcode = '#'+''.join(map(chr, rgb)).encode('hex')
                    #print hexcode
                    h,s,v = rgb2hsv(r,g,b)
                    currenthuegroup = int(h/6)
                    huefreq[currenthuegroup]= huefreq[currenthuegroup]+1
           # print huefreq                

            latlng = str(file).split("_")
            lat = latlng[-3].split("/")[-1]
            lng = latlng[-2]
            #print lat, lng
            imagedata = [lat, lng, huefreq]
            #print imagedata
            spamwriter.writerow(imagedata)