import Image
import math
import csv
image = Image.open("aberdeen_grid.jpg")
pix = image.load()
width, height = image.size
values = []
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
    
with open ("test.csv", "wb") as coloroutput:
    filewriter = csv.writer(coloroutput)
    for x in range(1,width):
        if x%10==0:
            print x
        for y in range(1,height):
            #print pix[x,y]
            r,g,b = pix[x,y]
            rgbsum = r+g+b
            h,s,v = rgb2hsv(r,g,b)
            #print r,g,b, rgbsum, h,s,v
            value = {"r":r,"g":g,"b":b,"rgbsum":rgbsum,"h":round(h,2),"s":round(s,2),"v":round(v,2)}
           # values.append(value)
            #print value
            filewriter.writeline(str(value))
#valuefreq = {}
#for value in values:
 #   valuesfreq[value]=valuesfreq.get(value,1)+1
 #   print value