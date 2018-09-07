import math
import urllib
import urllib2
from StringIO import StringIO
import requests
import time

# topLeft, bottomRight  = [lat, lng], 
# numPoints in each row/column, so numPoints = 10 will give you a 10x10 grid.
 
i = 0 
j = 0
heading = 0
pitch = 10
fov = 90
name = "a"

#latitude = 42.364128
#longitude = -71.103187

def makeGrid(topLeft, bottomRight, numPoints):
	topLat = topLeft[0]
	leftLng = topLeft[1]
	bottomLat = bottomRight[0]
	rightLng = bottomRight[1]
	horizontal_offset = (compute_distance(topLeft, [topLat, rightLng])/numPoints)
	vertical_offset = (compute_distance(topLeft, [bottomLat, leftLng])/numPoints)
	#print horizontal_offset, vertical_offset
 
	pointer = topLeft
	rowheader = topLeft
	grid = [pointer]
	for i in range(numPoints):
		for j in range(numPoints):
			next = compute_offset(pointer, horizontal_offset, 90)	
			grid.append(next)
			pointer = next
		rowheader = compute_offset(rowheader, vertical_offset, 180)
		pointer = rowheader
	for row in grid:
		for j in range(1):
			heading = j*90
			createStreetViewURL(row[0], row[1], heading, pitch, fov, name)
			time.sleep(1.8)
			i = i+1
			print heading
	return grid
	
## Helper functions for makeGrid
 
def degrees_to_radians(degrees):
	return degrees * math.pi /180;
 
def radians_to_degrees(radians):
	return radians  *  180 / math.pi
 
def compute_distance(p1, p2):
	[lat1, long1] = p1
	[lat2, long2] = p2
	degree_to_radians = math.pi/180
	dist_to_miles = 3960
	dist_to_kms = 6371.01
 
	#phi = 90 - latitude
	phi1 = (90.0 - lat1)* degree_to_radians
	phi2 = (90.0 - lat2)* degree_to_radians
 
	#theta = longitude
	theta1 = long1*degree_to_radians
	theta2 = long2*degree_to_radians
 
	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1-theta2) + math.cos(phi1)*math.cos(phi2))
	arc = math.acos(cos)
 
	return arc * dist_to_miles
	
def compute_offset(startPoint, distance, bearing):
	lat = startPoint[0]
	lng = startPoint[1]
 
	# in miles. divide by 6371.01for kms
	distRatio = distance/ 3960
 
	distSine = math.sin(distRatio)
	distCosine = math.cos(distRatio)
 
 
	bearing = degrees_to_radians(bearing)
	startLatRad = degrees_to_radians(lat)
	startLngRad = degrees_to_radians(lng)
	startLatCos = math.cos(startLatRad)
	startLatSin = math.sin(startLatRad)
 
	endLatRads = math.asin((startLatSin * distCosine) + (startLatCos * distSine * math.cos(bearing)))
	endLonRads = startLngRad + math.atan((math.sin(bearing) * distSine * startLatCos)/(distCosine - startLatSin * math.sin(endLatRads)));
 
 
	finalLat = radians_to_degrees(endLatRads)
	finalLng = radians_to_degrees(endLonRads)
	return [finalLat, finalLng]

def downloadImage(query_url, filename, root_dir="/Users/jiazhang/Documents/GitHub/streetviewcolor/NewYork5/"):
    response = requests.get(query_url)
    localfile = open(root_dir + str(filename) + '.jpeg', 'w')
    localfile.write(response.content)
    localfile.close()




def createStreetViewURL(latitude, longitude,heading,pitch, fov, outputfilename , api_key='AIzaSyBZnvqy9HEpG-LAQwm_AxDOegMciI9jgP4'):
    url = 'http://maps.googleapis.com/maps/api/streetview?size=640x640&location='+str(latitude)+','+str(longitude)+'&fov='+str(fov)+'&heading='+str(heading)+'&pitch='+str(pitch)+'&sensor=false&key='+api_key
    filename = str(latitude) + '_' + str(longitude) + '_' + str(heading)
    downloadImage(url,filename)

makeGrid([40.736516,-74.0075864066],[40.7628541651,-73.9656092319], 100)
#createStreetViewURL(latitude, longitude, heading, pitch, fov, name)
