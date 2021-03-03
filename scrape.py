#importing package
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
import re

#Get user input
what = input('What industry are you looking to get numbers for?')
where = input('give me a zip code')
#Change to apporpriate data type
what = str(what)
where = int(where)
#Making url's more usable
fixedwhat = what.replace(' ', '+')
#lists that will be amendided as needed
name_list = []
phone_list = []
address = []
x=0
for run_10 in range (10):
    x = x + 1
    url = f'https://www.yellowpages.com/search?search_terms={fixedwhat}&geo_location_terms={where}&page={x}'
    #Get HTML and parcer it
    html = requests.get(url).text
    soupurl = BeautifulSoup(html, features="html.parser")



    for findcard in soupurl.find_all('div', class_="v-card"):
        #Declaring global varibles
        global wo_span_name
        global wo_div_phone
        global wo_dive_adress_fl
        global wo_dive_adress_sl
        global full_adress
        full_adress = None
        #grab name
        w_span_name = findcard.find('a', class_='business-name')
        wo_span_name = w_span_name.text
        #grab phone number

        w_div_phone = findcard.find('div', class_="phones phone primary")
        w1_div_phone = str(w_div_phone)
        wo_div_phone = re.sub('\D', '', w1_div_phone)

        #Grab adress
        try:
            w_dive_adress_fl = findcard.find('div', class_="street-address")
            w_dive_adress_sl = findcard.find('div', class_="locality")
            wo_dive_adress_fl  = w_dive_adress_fl.text
            wo_dive_adress_sl = w_dive_adress_sl.text
            full_adress = wo_dive_adress_fl +' ' + wo_dive_adress_sl
        except:
            print('no address')
        try:
            address.append(full_adress)
            phone_list.append(wo_div_phone)
            name_list.append(wo_span_name)
        except:
            print('invalidvcard')

#Turning lists into array
name_array = np.array(name_list)
phone_array = np.array(phone_list)
address_array = np.array(address)
#creating the data frame from the lists
List_with_none = pd.DataFrame({'name': name_array, 'phone': phone_array, 'address' : address_array }, columns=['name', 'phone', 'address'])
#Removing None Items
List_with_none['phone'].replace('', np.nan, inplace=True)
updated_list_complete = List_with_none.dropna(axis = 0, how ='any')
#Making rows readable
updated_list_complete.index = updated_list_complete.index + 1
#exporting to csv
updated_list_complete.to_csv(r'C:\Users\Michael\Desktop\newfolder\newstorage.csv')
