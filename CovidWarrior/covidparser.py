# import requests
from bs4 import BeautifulSoup
import csv
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

URL = "https://covidwarriors.gov.in/default.aspx"
base_url =  "https://covidwarriors.gov.in/"
r = urllib.request.urlopen(URL)

# browser = webdriver.PhantomJS()
# browser.get(URL)
# html = browser.page_source

options = Options()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('w3c', False)
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=options, chrome_options=chrome_options)
browser.get(URL)
browser.implicitly_wait(5)
mySelect = Select(browser.find_element_by_name("ddlstate"))
# mySelect = Select(driver.find_element_by_id("mySelectID"))
final_result = {}
for o in range(2,len(mySelect.options)):
        browser.get(URL)
        mySelect = Select(browser.find_element_by_name("ddlstate"))
        mySelect.select_by_index(o)
        browser.get(URL)
        # browser.implicitly_wait(20)
        soup = BeautifulSoup(browser.page_source,"html.parser")
        header = soup.find('h4')
        header_text = str(header.text).replace('\n','').replace('  ','')
        final_result[header_text] = []
        table = soup.findAll('div', attrs = {'class':'scheme-block'})
        for row in table:
#     # print(row)
                org_name = row.find('b',attrs = {'class':'org_name'})
                label = row.find('div',attrs = {'class':'label_heads'})
                total_number = label.findAll('a')
                for a_tag in total_number:
                        if '.aspx' in str(a_tag.get('href')):
                                final_result[header_text].append({'Category': str(org_name.text).replace('\n','').replace('  ',''),'value': str(a_tag.text).replace('\n','').replace('  ',''),'SubCategory': {}})
                                browser.get(base_url+str(a_tag.get('href')))
                                browser.implicitly_wait(10)
                                subsoup = BeautifulSoup(browser.page_source,"html.parser")
                                # print(subsoup)
                                subcategory = {}
                                sub_header = subsoup.find('h4')
                                sub_header_text = str(sub_header.text).replace('\n','').replace('  ','')
                                subcategory[sub_header_text] = []
                                sub_table = subsoup.findAll('div', attrs = {'class':'scheme-block'})
                                for sub_row in sub_table:
                                        sub_org_name = sub_row.find('b',attrs = {'class':'org_name'})
                                        sub_label = sub_row.find('div',attrs = {'class':'label_heads'})
                                        sub_total_number_a = sub_label.find_all('a')
                                        for sub_a_tag in sub_total_number_a:
                                                if '.aspx' in str(sub_a_tag.get('href')):
                                                        subcategory[sub_header_text].append({'Category': str(sub_org_name.text).replace('\n','').replace('  ',''),'value': str(sub_a_tag.text).replace('\n','').replace('  ','')})
                                final_result[header_text][len(final_result[header_text])-1]['SubCategory'] = subcategory

import json
import datetime
st_date = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
with open('covid_warriors_data_'+str(st_date)+'.json', 'w', encoding='utf-8') as f:
        json.dump(final_result, f, ensure_ascii=False, indent=4)