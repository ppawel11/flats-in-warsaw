import bs4 as bs
import urllib.request as req
import time
import csv
import sys

def str_to_int(text):
	result = ''.join(char for char in text if char.isdigit())
	if len(result):
		return int(result)
	return None

def gener_url(n):
	n = str(n)
	url = "https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/warszawa/"
	if n != "1": url += "page-"+n+"/"
	url += "v1c9008l3200008p"+n
	return url

def get_flats(pages):
	flats = []
	for page_id in range(1,pages+1):
		try:
			page = req.Request(gener_url(page_id), headers={'User-Agent': 'Mozilla/5.0'})
			sauce = req.urlopen(page).read()
			soup = bs.BeautifulSoup(sauce,'lxml')
		except:
			continue

		flats_view = soup.find_all("div", {"class": "tileV1"})		
		for titleV1 in flats_view:
			flats.append(titleV1.find("div", {"class": "title"}).find("a")['href'])
	
	print("Zbieranie adresów url mieszkań zakończone")
	print("zebrano:\t", len(set(flats)))
	return set(flats)

def get_data(url):
	flat = dict()
	flat['url'] = "https://www.gumtree.pl" + url
	try:
		page = req.Request(flat['url'], headers={'User-Agent': 'Mozilla/5.0'})
		sauce = req.urlopen(page).read()
		soup = bs.BeautifulSoup(sauce,'lxml')
	except:
		return None
	
	details = soup.find("div", {"class": "vip-header-and-details"})
	
	price = details.find("div", {"class": "price"}).find("span", {"class": "value"}).text.strip()
	if price.isalpha():
		flat['Cena'] = None
	else:
		flat['Cena'] = str_to_int(price)

	for div in details.find_all("div", {"class":"attribute"}):
		name = div.find("span",{"class": "name"}).text.strip()
		value = div.find("span",{"class": "value"}).text.strip()
		if name == 'Lokalizacja':
			value = value.split(',')[0]
		elif name == 'Liczba łazienek' or name == 'Wielkość (m2)':
			value = str_to_int(value)
		elif name == 'Liczba pokoi':
			if value == 'Kawalerka lub garsoniera':
				value = 1
			else:
				value = str_to_int(value)
		flat[name] = value
	return flat
	
if __name__ == '__main__':
	pages = 899
	if len(sys.argv)>1 and sys.argv[1].isdigit() and int(sys.argv[1]) < 899:
		pages = int(sys.argv[1])
	result = []
	start = time.time()
	for url in get_flats(pages):
		flt = get_data(url)
		if flt: result.append(flt)
	stop = time.time()
	
	#just a way to get fieldnames out of collected results:
	#fieldnames = set() 
	#for r in result:	
	#	for k in list(r.keys()):
	#		fieldnames.add(k)
	
	#but this is faster:
	fieldnames = ['Rodzaj nieruchomości', 'Lokalizacja', 'Cena', 'Wielkość (m2)', 'Liczba pokoi', 'Liczba łazienek', 'Parking', 'Przyjazne zwierzakom', 'Palący', 'Do wynajęcia przez', 'Dostępny od', 'Data dodania', 'url']

	if result:
		with open("flats_test.csv", "w") as csvfile:
			fieldnames = list(fieldnames)
			writer = csv.DictWriter(csvfile, fieldnames = fieldnames)	
			writer.writeheader()		
			writer.writerows(result)
		
		minutes = int((stop-start)//60)
		seconds = int((stop-start)%60)
		print("\nzapisano", len(result)," mieszkań")
		print("CZAS:\t",minutes," min ", seconds, " s")
	else:
		print("Coś poszło nie tak. Plik csv nie został utworzony.")

