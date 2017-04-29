import pandas as pd
import requests, time, csv, datetime
import urllib2
from bs4 import BeautifulSoup 
import re, urllib
from random import randint

def find_text(lines):
	output=[]
    	for line in lines:
    		for l in line:
        		output.append(str(l.text).strip('\n'))
    	return output
  	

def count_total_page(in_city):
	city_temp = (in_city[0],'search/cto')
	
	city_url = ''.join(city_temp)
	response_city =requests.get(city_url,proxies=proxies)
	city1=response_city.content

	soup_city=BeautifulSoup(city1)
	output = soup_city.find_all('span', {'class' : 'totalcount'})
	output2 = output[0].text
	return int(output2)//100+1
  
##Purchase and set up the Proxies :  
proxies = {'http': 'http://zhaoruyi666:wsnbb678@us-il.proxymesh.com:31280', 'https': 'http://zhaoruyi666:wsnbb678@us-il.proxymesh.com:31280'}

	
all_cars=[]  
with open("/Users/Ruyi/Desktop/craigslist/city_name_new.csv",'rU') as file:
	reader = csv.reader(file)
	
	for city in list(reader)[2:3]:
		
		page_count= count_total_page(city)
		print page_count
		all_cars=[]
		for i in range(0,page_count//2):
			if i == 0:
				url_temp1 = (city[0],'search/cto?s=')
				search_url0 = ''.join(url_temp1)
				response =requests.get(search_url0, proxies=proxies)

			else:	
				i_100 = str(i*100)
				url_temp = (search_url0,i_100)
				search_url1 = ''.join(url_temp)
				response =requests.get(search_url1, proxies=proxies)
			step1=response.content


			html_name_t = ("/Users/Ruyi/Desktop/craigslist/html/", str(datetime.datetime.today().strftime('%Y-%m-%d')),"_",str(i))
			html_name = ''.join(html_name_t)
			
			file=open(html_name,"w")
			file.write(step1)
			file.close()
				
			response2 =urllib.urlopen(html_name)
				
			step11=response2.read()
			soup=BeautifulSoup(step11)
			id_list=[]
			for link in soup.find_all('a',{'class' : 'result-image gallery'}):
				id_list.append(link['href'][1::])
				
			idall=set(id_list)			
			#idall=['cto/5992760672.html']		
			cars=[]

			d_year={}
			d_make={}
			d_model={}
			d_price={}
			d_notes={}
			d_city={}
			d_more={}
			for k, url in enumerate(idall):
				try:
					url_all=(city[0], url)
					url_x=''.join(url_all)
					x =requests.get(url_x, proxies=proxies).content
					html=BeautifulSoup(x)
					#print html
					print url_x 
					items = html.find_all('p', {'class' : 'attrgroup'})
					#print items
					bodies = html.find_all('section', {'id' : 'postingbody'})
					#print bodies
					price = html.find_all('span', {'class' : 'price'})
					#print price
					contents = [items,bodies,price]	
					item=find_text(contents)
					
					ymm = item[0].split(' ')
					d_year['Year'] = ymm[0]		
					d_make['Make'] = ymm[1]		
					d_model['Model'] = ' '.join(ymm[2:])
					d_more=dict(x.split(':') for x in item[1].split('\n'))		
					d_price['Price'] = item[3]		
					d_notes['Notes'] = item[2]
					d_city['City']	= city[1]		
					d_all = dict(d_year.items() + d_make.items() + d_model.items() + d_more.items() + d_price.items() + d_notes.items() + d_city.items())
   					time.sleep(randint(1,3))
					cars.append(d_all)
					print str(page_count) + city[1] + str(i) + "_" + str(k)
			
				except:
					pass	
			all_cars.append(cars)
		csv_temp = ('/Users/Ruyi/Desktop/craigslist/results/',city[1],'_1.csv')
		csvname = ''.join(csv_temp)
		with open(csvname, 'w') as csvfile:
			fieldnames = ['Year', 'Make', 'Model', 'title status', 'VIN', 'odometer', 'transmission', 'paint color', 'fuel', 'Price', 'condition', 'cylinders', 'drive', 'type', 'size' , 'Notes', 'City']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for line in all_cars:
				for item in line:
					writer.writerow(item)
		
		execfile('/Users/Ruyi/Desktop/cleanup.py')
		
		for i in range(page_count//2,page_count):
			if i == 0:
				url_temp1 = (city[0],'search/cto?s=')
				search_url0 = ''.join(url_temp1)
				response =requests.get(search_url0, proxies=proxies)

			else:	
				i_100 = str(i*100)
				url_temp = (search_url0,i_100)
				search_url1 = ''.join(url_temp)
				response =requests.get(search_url1, proxies=proxies)
			step1=response.content


			html_name_t = ("/Users/Ruyi/Desktop/craigslist/html/", str(datetime.datetime.today().strftime('%Y-%m-%d')),"_",str(i))
			html_name = ''.join(html_name_t)
			
			file=open(html_name,"w")
			file.write(step1)
			file.close()
				
			response2 =urllib.urlopen(html_name)
				
			step11=response2.read()
			soup=BeautifulSoup(step11)
			id_list=[]
			for link in soup.find_all('a',{'class' : 'result-image gallery'}):
				id_list.append(link['href'][1::])
				
			idall=set(id_list)			
			#idall=['cto/5992760672.html']		
			cars=[]

			d_year={}
			d_make={}
			d_model={}
			d_price={}
			d_notes={}
			d_city={}
			d_more={}
			for k, url in enumerate(idall):
				try:
					url_all=(city[0], url)
					url_x=''.join(url_all)
					x =requests.get(url_x, proxies=proxies).content
					html=BeautifulSoup(x)
					#print html
					print url_x 
					items = html.find_all('p', {'class' : 'attrgroup'})
					#print items
					bodies = html.find_all('section', {'id' : 'postingbody'})
					#print bodies
					price = html.find_all('span', {'class' : 'price'})
					#print price
					contents = [items,bodies,price]	
					item=find_text(contents)
					
					ymm = item[0].split(' ')
					d_year['Year'] = ymm[0]		
					d_make['Make'] = ymm[1]		
					d_model['Model'] = ' '.join(ymm[2:])
					d_more=dict(x.split(':') for x in item[1].split('\n'))		
					d_price['Price'] = item[3]		
					d_notes['Notes'] = item[2]
					d_city['City']	= city[1]		
					d_all = dict(d_year.items() + d_make.items() + d_model.items() + d_more.items() + d_price.items() + d_notes.items() + d_city.items())
   					time.sleep(randint(1,3))
					cars.append(d_all)
					print str(page_count) + city[1] + str(i) + "_" + str(k)
			
				except:
					pass	
			all_cars.append(cars)
		csv_temp = ('/Users/Ruyi/Desktop/craigslist/results/',city[1],'_2.csv')
		csvname = ''.join(csv_temp)
		with open(csvname, 'w') as csvfile:
			fieldnames = ['Year', 'Make', 'Model', 'title status', 'VIN', 'odometer', 'transmission', 'paint color', 'fuel', 'Price', 'condition', 'cylinders', 'drive', 'type', 'size' , 'Notes', 'City']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for line in all_cars:
				for item in line:
					writer.writerow(item)
		
		execfile('/Users/Ruyi/Desktop/cleanup.py')		
		
		
