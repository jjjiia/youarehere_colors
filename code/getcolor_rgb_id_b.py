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
for path, subirs, files in os.walk(r'/Users/jiazhang/Documents/GitHub/streetviewcolor/NewYork_40.734641_-74.028038_40.701854_-73.969072'):
    currentdir = []
    files = [f for f in files if not f[0] == '.']
    for filename in files:
        #JOIN NAME WITH PATH
        f = os.path.join(path, filename)
        currentdir.append(f)       
    print currentdir
values = []
#MAKE DICTIONARY
valuefreq={}
#OPEN FILES IN LIST AND GET COLOR
all_values = []
clusters = [(255,0,0),(0,255,0),(0,0,255)]
for file in currentdir:
    #print file
    redcount = 0
    bluecount = 0
    greencount = 0
    image = Image.open(file)
    width, height = image.size
    imgstat = os.stat(file)
    pix = image.load()
    #print imgstat[6]
    #CHECK IF IMAGE IS BLANK, AND REMOVE
    if imgstat[6] < 4483:
        os.remove(file)
    for x in range(0,width):
        for y in range(0,height):
            minDistance = 1000
            
            r,g,b = pix[x,y]
            rgb = (r,g,b)
            hexcode = '#'+''.join(map(chr, rgb)).encode('hex')
            #print hexcode
            h,s,v = rgb2hsv(r,g,b)
            # print imgstat, file
            #value = r, g, b, h, s, v, hexcod
            for cluster in clusters:
                d = math.sqrt(math.pow(r-cluster[0],2)+math.pow(g-cluster[1],2)+math.pow(b-cluster[2],2))
#                print cluster, d
                if d < minDistance:
                    minDistance = d
                    minCluster = cluster
            print minCluster, minDistance
                
    latlng = str(file).split("_")
    #print latlng
    total = redcount+greencount+bluecount
    imagestat = [redcount, greencount, bluecount,total, latlng[1], latlng[2][0:-5]]
    all_values.append(imagestat)
#print all_values
basepath = '/Users/jiazhang/Documents/GitHub/streetviewcolor/'
with open(basepath+'eggs.csv', 'w') as csvfile:
    print "open"
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(all_values)