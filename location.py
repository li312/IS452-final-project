import csv
from geopy.geocoders import Nominatim
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
    outfile=open("location4.txt","w")
    for list in cordlist[401+93+2201:]:
        coordinate=list[0]+","+list[1]
        geolocator=Nominatim()
        location = geolocator.reverse(coordinate)
        print(location.address)
        print(location.address,file=outfile)

def main():
    infile=open("offense.csv","r")
    s=csv.reader(infile)

    location(s)
    #crimeType(s)
    #getNumCrime()
    #CrimeEachYear()
    infile.close()

main()
