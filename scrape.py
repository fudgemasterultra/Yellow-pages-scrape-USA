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
        #grab name
        w_span_name = findcard.find('a', class_='business-name')
        wo_span_name = w_span_name.text
        #grab phone number

        w_div_phone = findcard.find('div', class_="phones phone primary")
        w1_div_phone = str(w_div_phone)
        wo_div_phone = re.sub('\D', '', w1_div_phone)


        phone_list.append(wo_div_phone)
        name_list.append(wo_span_name)

#Turning lists into array
name_array = np.array(name_list)
phone_array = np.array(phone_list)
#creating the data frame from the lists
List_with_none = pd.DataFrame({'name': name_array, 'phone': phone_array }, columns=['name', 'phone'])
#Removing None Items
List_with_none['phone'].replace('', np.nan, inplace=True)
updated_list_complete = List_with_none.dropna(axis = 0, how ='any')
#Making rows readable
updated_list_complete.index = updated_list_complete.index + 1
#exporting to excel
#print(updated_list_complete)
updated_list_complete.to_csv(r'c:\File Name.csv')

