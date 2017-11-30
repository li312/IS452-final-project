import csv
import _thread
from collections import Counter
from geopy.geocoders import Nominatim
def getNumCrime():
    with open("offense.csv","r") as offenseCsvfile:
        content=csv.reader(offenseCsvfile)
        next(content,None)
        count=0
        for row in content:
            count+=1
    print(count)
    offenseCsvfile.close()
def CrimeEachYear():
    list=[]
    with open("offense.csv","r") as offenseCsvfile:
        content=csv.reader(offenseCsvfile)
        next(content,None)
        for row in content:
            list.append(row[2][0:4])

    Crimedict=dict(Counter(list))
    print(Crimedict)
    offenseCsvfile.close()
def crimeType(s):
    list=[]
    next(s,None)
    for row in s:
        list.append(row[1][6:])
    Crimetype=dict(Counter(list))
    print("The Crime type")
    for key in Crimetype:
        print(key+" has " + str(Crimetype[key])+ " times")

def location(s):
    cordlist=[]
    next(s,None)
    for row in s:

        list=[]
        try:
            list.append(row[6])
            list.append(row[5])
            cordlist.append(list)
        except:
            break
    for list in cordlist:
        coordinate=list[0]+","+list[1]
        geolocator=Nominatim()
        location = geolocator.reverse(coordinate)
        print(location.address)

def main():
    infile=open("offense.csv","r")
    s=csv.reader(infile)
    
    #location(s)
    #crimeType(s)
    #getNumCrime()
    #CrimeEachYear()
    infile.close()

main()
