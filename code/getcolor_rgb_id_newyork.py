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
    for path, subirs, files in os.walk(r'/Users/jiazhang/Documents/GitHub/streetview_downloader/manhattan-split/images-'+str(folderNumber)):
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
    valuefreq={}
    #OPEN FILES IN LIST AND GET COLOR
    basepath = '/Users/jiazhang/Documents/GitHub/streetviewcolor/'
    with open(basepath+'manhattan_'+str(folderNumber)+'.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        print "open"
        for file in currentdir:
            #print file
            redcount = 0
            bluecount = 0
            greencount = 0
            samecount = 0
        
            redgreen = 0
            redblue = 0
            greenblue = 0
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
                    # print imgstat, file
                    #value = r, g, b, h, s, v, hexcod
                    redness = math.sqrt(math.pow((float(r)-255),2)+math.pow(float(g),2)+math.pow(float(b),2))
                    greeness = math.sqrt(math.pow((float(g)-255),2)+math.pow(float(r),2)+math.pow(float(b),2))
                    blueness = math.sqrt(math.pow((float(b)-255),2)+math.pow(float(g),2)+math.pow(float(r),2))
                    #print redness, greeness, blueness
                    if redness < greeness and redness < blueness:
                        #print "red"
                        redcount = redcount+1
                    elif greeness < redness and greeness < blueness:
                        #print "green"
                        greencount = greencount+1
                    elif blueness < redness and blueness < greeness:
                        #print "green"
                        bluecount = bluecount+1
                    elif redness == greeness and redness == blueness:
                        samecount = samecount+1
                    elif redness == greeness and redness < blueness:
                        #redcount = redcount+1
                        #greencount = greencount+1
                        redgreen = redgreen+1
                    elif redness == blueness and redness < greeness:
                        #redcount = redcount+1
                        #bluecount = bluecount+1
                        redblue = redblue+1
                    elif greeness == blueness and greeness < redness:
                        greenblue = greenblue+1
                        #print "r"+r, g, b
                    #else:
                       # print redness, greeness, blueness
                    
            latlng = str(file).split("_")
            lat = latlng[-3].split("/")[-1]
            lng = latlng[-2]
            #print lat, lng
            total = redcount+greencount+bluecount+samecount+greenblue+redblue+redgreen
            imagedata = [redcount, greencount, bluecount, samecount, redgreen, redblue, greenblue, total, lat, lng]
            #print imagedata
            spamwriter.writerow(imagedata)