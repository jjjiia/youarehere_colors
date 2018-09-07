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
for path, subirs, files in os.walk(r'/Users/jiazhang/Documents/GitHub/streetviewcolor/lowerManhattan'):
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
for file in currentdir:
    print file
    #print file
    #file = "/Users/jiazhang/Desktop/test.jpg"
    image = Image.open(file)
    width, height = image.size
    imgstat = os.stat(file)
    pix = image.load()
    #print imgstat[6]
    #CHECK IF IMAGE IS BLANK, AND REMOVE
    if imgstat[6] == 4483:
        os.remove(file)
    for x in range(0,width):
        for y in range(0,height):
            r,g,b = pix[x,y]
            rgb = (r,g,b)
            hexcode = '#'+''.join(map(chr, rgb)).encode('hex')
            #print hexcode
            h,s,v = rgb2hsv(r,g,b)
            # print imgstat, file
            value = r, g, b, h, s, v, hexcode
            #print value
            if (value in valuefreq):
                #print "yes"
                valuefreq[value] = valuefreq.get(value,0)+1
            else:
                valuefreq[value] = 0
                #print "no"
#print len(valuefreq)
newvaluefreq = []
for key, value in valuefreq.iteritems():
    if value > 100:
        temp = {
            "r":str(key[0]),
            "g":str(key[1]),
            "b":str(key[2]),
            "h":str(key[3]),
            "s":str(key[4]),
            "v":str(key[5]),
            "name":str(key[6]),
            "size": str(value)     
        }
        newvaluefreq.append(temp)
#print len(newvaluefreq)
print "{\"name\":\"flare\", \"children\":", newvaluefreq, "}"