import csv
from collections import Counter
from geopy.geocoders import Nominatim
from geopy.distance import vincenty

def getNumCrime():
    infile=open("offense.csv","r")
    offense=csv.reader(infile)
    next(offense,None)
    count=0
    for row in offense:
        count+=1
    infile.close()
    print("\nThe total crime number is "+str(count))
def CrimeEachYear():
    list=[]
    infile=open("offense.csv","r")
    offense=csv.reader(infile)
    next(offense,None)
    for row in offense:
        list.append(row[2][0:4])

    Crimedict=dict(Counter(list))
    infile.close()
    print("\nFollowing are crimes each year")
    print(Crimedict)
def crimeType():
    list=[]
    infile=open("offense.csv","r")
    offense=csv.reader(infile)
    next(offense,None)
    for row in offense:
        list.append(row[1][6:])
    Crimetype=dict(Counter(list))
    infile.close()
    print("\nThe Crime type")
    for key in Crimetype:
        print(key+" has " + str(Crimetype[key])+ " times")

def location():
    cordlist=[]
    infile=open("offense.csv","r")
    offense=csv.reader(infile)
    next(offense,None)
    for row in offense:

        list=[]
        try:
            list.append(row[6])
            list.append(row[5])
            cordlist.append(tuple(list))
        except:
            break

    coordinate_count=Counter(cordlist)
    coordfile=open("coordfile.txt","w")
    addressfile=open("addressfile.txt","w")
    print("\nThe Top 10 dangerous places are: ")
    for coord in coordinate_count.most_common(10):
        coordinate=coord[0][0]+","+coord[0][1]
        geolocator=Nominatim()
        location = geolocator.reverse(coordinate)

        print(coordinate,file=coordfile)
        print(location.address,file=addressfile)
        #print("\nThe Top 10 dangerous places are: ")
        print(location.address)
    coordfile.close()
    addressfile.close()
    infile.close()
def isLocationChange():
    infile=open("72hr.csv","r")

    policeCall=csv.reader(infile)
    next(policeCall,None)
    locationList=[]
    for row in policeCall:
        locationList.append(row[3])
    infile.close()
    addressfile=open("addressfile.txt","r")
    addresslist=[]
    for address in addressfile:
        addresslist.append(address)
    location_Count=Counter(locationList)

    for location in location_Count.most_common(10):

        for address in addresslist:
            if location[0].split(' ')[0] in address:
                print("\n"+address+" is still dangerous.")
def distPolice():
    policeStation="557 S Newtowne Dr, Rockford"
    stationList=[]
    geolocator=Nominatim()
    location = geolocator.geocode(policeStation)
    stationList.append((location.latitude,location.longitude))
    cordfile=open("coordfile.txt","r")
    addressfile=open("addressfile.txt","r")
    addressList=[]
    for address in addressfile:
        addressList.append(address)

    addresscount=0
    for cord in cordfile:
        cord=cord.split(",")
        cord=tuple(map(float,cord))
        print("\nThe distance between "+"Police station"+
                  " and "+addressList[addresscount]+"is: "+str(vincenty(cord,stationList[0]).miles)+" miles.")
        addresscount+=1

def main():


    moreFunction="yes"
    while moreFunction[0]=="y":
        function=input("\nWhat do you want to see?:  \n a.number of crimes\n b.number of crime each year\n c.crime type\n d.top 10 dangerous place\n e.distance between police station and the place\n f.if the dangerous places changes comparing to recent police phone call ")
        if function.lower()=="a":
            getNumCrime()
        if function.lower()=="b":
            CrimeEachYear()
        if function.lower()=="c":
            crimeType()
        if function.lower()=="d":
            location()
        if function.lower()=="e":
            distPolice()
        if function.lower()=="f":
            isLocationChange()
        moreFunction=input("\nDo you want to continue? ")



main()
