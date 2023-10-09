from requests_html import HTMLSession
import psutil, os, requests, shutil, re
from bs4 import BeautifulSoup
import wikipedia as wp
import rembg

print("Finding your location")
try:  # Geolocate the user based on MAC addresses of this and connected devices. Will work when not connected with less accuracy
    while True:
        macs = []
        for interface in psutil.net_if_addrs():
            if psutil.net_if_addrs()[interface][0].address:
                macs.append(psutil.net_if_addrs()[interface][0].address)
        macs = [m for m in macs if (0 == (2 & int(m[1], 16)) and m[:8].upper() != '00:00:5E')]
        if len(macs) >= 1:
            break
except:
    print("Error getting Mac addresses")
    exit()

try:
    json = {
        "considerIp": "true",
        "wifiAccessPoints": []
    }
    for address in macs:
        json["wifiAccessPoints"].append({"macAddress": address})
except:
    print("Error building location request")
    exit()

try:
    with open("request.json", "w+") as file:
        # print(json)
        file.write(str(json))
        api = "AIzaSyCtbWU68h372AF7bdOseSh3okC9H3j_mng"
        x = requests.post("https://www.googleapis.com/geolocation/v1/geolocate?key=" + api, file)
except:
    print('Error getting location data')
    exit()
try:
    os.remove("request.json")
except:
    pass
lat = x.text[30:40].replace(",", "")
lng = x.text[52:63].replace(",", "")


def getSearchArea(inLat, inLong, size):  # Return Coordinates in a {size} mile square around the user's location
    search = size / 2
    return (inLat + (search / 69), inLong + (search / 54.6), inLat - (search / 69), inLong - (search / 54.6))


def buildURL(inLat, inLong, size):  # Use the coordinates to search the area on inaturalist
    coords = getSearchArea(inLat, inLong, size)
    return "https://www.inaturalist.org/observations?iconic_taxa=Amphibia,Actinopterygii,Mollusca&nelat=" + str(
        coords[0]) + "&nelng=" + str(coords[1]) + "&place_id=any&swlat=" + str(coords[2]) + "&swlng=" + str(
        coords[3]) + "&view=species"


size = 20
#lat, lng, size = 38.1380, -92.8104, 8 # Testing coordinates in the Lake of the Ozarks, uncomment for testing if local results show nothing.
url = buildURL(float(lat), float(lng), size)
print("Location found. Beginning search, please be patient.")

count = 0
while count < 50:  # Allow 50 attempts to load search data.
    session = HTMLSession()
    x = session.get(url)
    x.html.render()
    if x.status_code == 200:
        x = BeautifulSoup(x.html.html, "html.parser")
        x = x.find_all('div', attrs={"taxa-grid": "taxa-grid"})
        names = []
        imglinks = []
        for i in x:
            list = i.find_all('a', attrs={"class": re.compile("com")})  # Find html elements representing animals
            if list:
                for n in list:
                    names.append(n.text.replace("Species", "").replace("\n", "").replace("UnknownGenus",""))  # Clean up the returned names

        imglinks = []
        for i in x:
            list = i.find_all('a', attrs={"class": "photo"})
            if list:
                for n in list:
                    imglinks.append(n["style"].replace("background-image: url(\"", "").replace("\");", ""))

        if len(names) > 0:  # Stop looping once we get results
            break
        else:
            count += 1

if names == []:
    print("No nearby aquatic animals found")
    exit()

print("Located " + str(len(names)) + " nearby aquatic animals, retrieving information.\n")




def getAnimalInfo(animal):  # Use wikipedia api to find info on the animal
    pages = wp.search(animal)
    page = wp.page(pages[0], auto_suggest=False)
    summary = page.summary  # Find wikipedia summary of the animal
    return (summary, page.url)


class animal:
    def __init__(self, name, info, url, image):
        self.name = name
        lines = info.split(" ")
        self.info = ""
        self.url = url
        for i in range(50):  # Store first 50 words of wikipedia summary
            try:
                self.info += lines[i]
                self.info += " "
            except:
                pass
        self.info += "... (" + self.url + ")"  # Add a link to the wikipedia page for more information
        self.imagelink = image


def createAnimals(animals, images):  # Create animal classes based on the names returned from our inaturalist search
    aquarium = []
    for a in animals:
        info = getAnimalInfo(a)
        img = images[animals.index(a)]
        aquarium.append(animal(a, info[0], info[1], img))
    return aquarium


atest = names
aqtest = createAnimals(atest, imglinks)


animalFolder = os.path.join(os.getcwd(), "Animals")

try:  # set up animal file tree
    shutil.rmtree(animalFolder)
except Exception as e:
    print(e)
    pass
if not os.path.exists("animalFolder"):
    os.mkdir("Animals")
for a in aqtest:
    name = a.name.replace(" ", "")
    newAnimal = os.path.join(animalFolder, name)
    if not os.path.exists("newAnimal"): os.mkdir(newAnimal)  # create a folder for each animal
    try:
        with open("Animals/" + name + "/summary.txt", "w") as file:  # add summary file to the animal folder
            file.write(a.info)
    except:
        pass
    with open("Animals/" + name + "/image.jpg", "wb") as file:  # add image to the animal folder
        imag = requests.get(a.imagelink).content
        file.write(rembg.remove(imag))

print("Animal data has been saved to " + animalFolder)