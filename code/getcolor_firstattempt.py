import os
import os.path
import Image
import math
import csv

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

newdir = []
#MAKE LIST OF FILES IN A DIRECTORY
for path, subirs, files in os.walk(r'/Users/jiazhang/Desktop/cambridge_streets/ames'):
    currentdir = []
    for filename in files:
        #JOIN NAME WITH PATH
        f = os.path.join(path, filename)
        currentdir.append(f)     
    #print currentdir
    newdir = currentdir[1:]
    print newdir
values = []
#MAKE DICTIONARY
valuefreq={}
#OPEN FILES IN LIST AND GET COLOR
for file in currentdir:
    print file
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
            h,s,v = rgb2hsv(r,g,b)
            # print imgstat, file
            value = r, g, b, h, s, v
            #print value
            if (value in valuefreq):
                #print "yes"
                valuefreq[value] = valuefreq.get(value,0)+1
            else:
                valuefreq[value] = 0
                #print "no"
print len(valuefreq)
newvaluefreq = []
for key, value in valuefreq.iteritems():
    temp = {
        "red": key[0],
        "green":key[1],
        "blue":key[2],
        "h":key[3],
        "s":key[4],
        "v":key[5],
        "size": value       
    }
    newvaluefreq.append(temp)
print newvaluefreq