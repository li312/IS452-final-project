import csv
from collections import Counter
from geopy.geocoders import Nominatim
from geopy.distance import vincenty

def getNumCrime():
    #open the offense file
    infile=open("offense.csv","r")
    offense=csv.reader(infile)
    #omit the header
    next(offense,None)
    #initialize a count and increase 1 when iterate 1 row in the file
    # The final count will be the number of the crime
    count=0
    for row in offense:
        count+=1
    infile.close()
    print("\nThe total crime number is "+str(count))
def CrimeEachYear():
    #initialize an empty list
    list=[]
    #next three line is same as first function
    infile=open("offense.csv","r")
    offense=csv.reader(infile)
    next(offense,None)
    #iterate the each row in the file and then append the year(which can be extract by each row[2][0:4]) in the list
    for row in offense:
        list.append(row[2][0:4])
    #Use counter to count the number of each year and then put them in to the dictionary
    Crimedict=dict(Counter(list))
    infile.close()
    print("\nFollowing are crimes each year")
    print(Crimedict)
def crimeType():
    list=[]
    infile=open("offense.csv","r")
    offense=csv.reader(infile)
    next(offense,None)
    # iterate each row and append crimetype(can be extract by row[1][6:]) in an empty array
    for row in offense:
        list.append(row[1][6:])
    #Count the number of the each crime type
    Crimetype=dict(Counter(list))
    infile.close()
    print("\nThe Crime type")
    for key in Crimetype:
        #shows how many times occur for each crime type
        print(key+" has " + str(Crimetype[key])+ " times")

def location():
    # assign an empty list first
    cordlist=[]
    # same line as first function
    infile=open("offense.csv","r")
    offense=csv.reader(infile)
    next(offense,None)
    #iterate each row in the file
    for row in offense:
        # assign an empty list to store the current coordinate
        list=[]
        try:
            #row[6] is latitude and row[5] is longitude.
            # Then append the latitude and longitude to the list
            # Then append the "tuplelized "list to the cordlist so cordlist looks like [(12.3,3.455),....]
            list.append(row[6])
            list.append(row[5])
            cordlist.append(tuple(list))
        except:
            break
    #Count how many coordinates in the cordlist
    coordinate_count=Counter(cordlist)
    #Open 2 files called coordfile and addressfile for writting in
    coordfile=open("coordfile.txt","w")
    addressfile=open("addressfile.txt","w")
    print("\nThe Top 10 dangerous places are: ")

    # iterate the top 10 most frequent coordinate
    for coord in coordinate_count.most_common(10):
        #convert the tuple to string: coord looks like ((1.234,5.5678),10)
        # So, coord[0][0] is 1.234, coord[0][1] is 5.5678. Then concatenate them with ','
        coordinate=coord[0][0]+","+coord[0][1]
        #use geopy API
        geolocator=Nominatim()
        # find the location
        location = geolocator.reverse(coordinate)

        #write the coordinate to the coordfile and write address to the address file.
        # address can be found in location.address
        print(coordinate,file=coordfile)
        print(location.address,file=addressfile)
        #print("\nThe Top 10 dangerous places are: ")
        print(location.address)
    coordfile.close()
    addressfile.close()
    infile.close()
def isLocationChange():
    #open the 72hr file
    infile=open("72hr.csv","r")

    policeCall=csv.reader(infile)
    next(policeCall,None)
    #assign an empty list
    locationList=[]
    for row in policeCall:
        #row[3] is the address in the 72hr file. Then append it to the locationList
        locationList.append(row[3])
    infile.close()
    #read the addressfile
    addressfile=open("addressfile.txt","r")
    addresslist=[]

    #iterate the addressfile and then put the top 10 address into an empty list
    for address in addressfile:
        addresslist.append(address)
    location_Count=Counter(locationList)

    #iterate the new top 10 frequent address in the location list which is from 72hr recent police call
    for location in location_Count.most_common(10):
        #iterate the old top 10 frequent address in the addresslist which is the crime from 2011 to 2016
        for address in addresslist:
            #find if the house number is in the old top 10 address. Then show it is still dangerous
            # location[0] is the address. Then splitting the space and finding the first element of the list would
            # find the house number.
            if location[0].split(' ')[0] in address:
                print("\n"+address+" is still dangerous.")
def distPolice():
    # This is the address of the police station
    policeStation="557 S Newtowne Dr, Rockford"
    stationList=[]
    #geopy API
    geolocator=Nominatim()
    location = geolocator.geocode(policeStation)
    # append the latitude and longitude to the stationList
    stationList.append((location.latitude,location.longitude))
    #read the coordfile and the addressfile
    cordfile=open("coordfile.txt","r")
    addressfile=open("addressfile.txt","r")
    #put the old top 10 address in the addresslist
    addressList=[]
    for address in addressfile:
        addressList.append(address)
    #initialize 0 to addresscount
    addresscount=0
    for cord in cordfile:
        # The cord is the coordinate in the coordile and it is a string, we need to convert it to tuple
        # First splite the ",". Now cord is a list with latitude and longitude
        cord=cord.split(",")
        #Then, we use map to convert the element type in the cord to float. Then, convert the list to tuple
        cord=tuple(map(float,cord))
        #addressList[addresscount] is the current address in the loop
        # vincenty is the method that compute the distance between 2 coordinates.
        print("\nThe distance between "+"Police station"+
                  " and "+addressList[addresscount]+"is: "+str(vincenty(cord,stationList[0]).miles)+" miles.")
        addresscount+=1

def main():

    #Initialized yes to a variable to make sure the while loop will run
    moreFunction="yes"
    while moreFunction[0]=="y":
        #list the function to let user to choose which one they want
        # user only need to type a, b or c...
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
        # ask the user if they want to continue the program after run one funcotion. If they type yes or y, it will continue
        # if other, the program will shut down
        moreFunction=input("\nDo you want to continue? ")



main()
