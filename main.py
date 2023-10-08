from requests_html import HTMLSession
import psutil, os
from bs4 import BeautifulSoup


try:
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
    for  address in macs:
        json["wifiAccessPoints"].append({"macAddress":address})
except:
    print("Error building location request")
    exit()

try:
    with open("request.json", "w+") as file:
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
lat = x.text[30:40].replace(",","")
lng = x.text[52:63].replace(",","")

def getSearchArea(inLat, inLong, size):
	search = size / 2
	return (inLat + (size / 69), inLong + (size / 54.6), inLat - (size / 69), inLong - (size / 54.6))

def buildURL(inLat, inLong, size):
	coords = getSearchArea(inLat, inLong, size)
	return "https://www.inaturalist.org/observations?iconic_taxa=Amphibia,Actinopterygii,Mollusca&nelat=" + str(coords[0]) + "&nelng=" + str(coords[1]) + "&place_id=any&swlat=" + str(coords[2]) + "&swlng=" + str(coords[3]) + "&view=species"

#lat, lng = 38.1380 , -92.8104
url = buildURL(float(lat), float(lng), 4)
print(url)
count = 0
while count < 10:
    session = HTMLSession()
    x = session.get(url)
    x.html.render()
    if x.status_code == 200:
        x = BeautifulSoup(x.html.html,"html.parser")
        x = x.find_all('div', attrs = {"taxa-grid":"taxa-grid"})
        names = []
        for i in x:
            list = i.find_all('a', attrs={"class":"display-name comname"})
            list += i.find_all('span', attrs={"class":"taxon genus Actinopterygii no-com-name"})
            list += i.find_all('span', attrs={"class": "taxon genus Amphibia no-com-name"})
            list += i.find_all('span', attrs={"class": "taxon genus Mollusca no-com-name"})
            if list:
                for n in list:
                    names.append(n.text.replace("Species","").replace("\n","").replace("UnknownGenus",""))
        if len(names) > 0:
            break
        else:
            count += 1

print(names)
import wikipedia as wp

def getAnimalInfo(animal):
	pages = wp.search(animal)
	page = wp.page(pages[0], auto_suggest=False)
	imgs = page.images
	summary = page.summary
	return (summary, imgs[0])

class animal:
	def __init__(self, name, info, image):
		self.name = name
		self.info = info
		self.imagelink = image

def createAnimals(animals):
	aquarium = []
	for a in animals:
		info = getAnimalInfo(a)
		aquarium.append(animal(a, info[0], info[1]))
	return aquarium

atest = names
aqtest = createAnimals(atest)
for a in aqtest: print(a.info)