from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # explicit waits
from selenium.webdriver.support import expected_conditions as EC # expected conditions
from selenium.webdriver.common.keys import Keys
from functools import reduce

import time # sleeptime
import datetime # for date
import re
import random

dateNow = datetime.datetime.now()
#driver = webdriver.Chrome()
chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images':2}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chromeOptions)
driver.get("https://www.ulta.com/makeup-face?N=26y3&No=0&Nrpp=96") # start url

import csv
filename=paste(['ulta_cosFace'], [dateNow.year], ['-'], [dateNow.month], ['-'], [dateNow.day], ['.csv'], sep='')
filename=''.join(filename)
csv_file=open(filename, 'w', encoding='utf-8', newline='')
writer=csv.writer(csv_file)
#@ writer.writerow(['title', 'text', 'username', 'date_published', 'rating']) # manual header input

waiTTT = WebDriverWait(driver, 10)
totalpage = 17
index = 1
cos_LinksAll = []
while True:
	if index > 17:
		break
	try:
		result_urls = ['https://www.ulta.com/makeup-face?N=26y3&No={}&Nrpp=96'.format(x * 96) for x in range(0, totalpage)]
		index +=1
		for url in result_urls:
			driver.get(url)
			cos_List = (driver.find_elements_by_xpath('//div[@class="prod-title-desc"]/p[@class="prod-desc"]/a'))
			cos_Links = [i.get_attribute('href') for i in cos_List]
			cos_LinksAll.extend(cos_Links)
			time.sleep((2.5) + (random.randint(0, 300) / 300))
	except Exception as e:
		print(e)
		continue
	print(len(cos_LinksAll))
for linkK in cos_LinksAll:
	ulta_dict={}
	driver.get(linkK)
	print(linkK)
	try:
		time.sleep((3) + (random.randint(0, 260) / 260))
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

		try:
			ulta_Name = driver.find_element_by_xpath(
				'//div/span[@class="Text Text--subtitle-1 Text--left Text--small Text--text-20"]').text
		except:
			print('Name missing.')
			ulta_Name = None
		try:
			ulta_Brand = driver.find_element_by_xpath(
				'//p[@class="Text Text--body-1 Text--left Text--bold Text--small Text--$magenta-50"]').text
		except:
			print('Brand missing.')
			ulta_Brand = None
		try:
			# waiTTT2 = WebDriverWait(driver, 18.87)
			webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
			plus_but = waiTTT.until(
				EC.element_to_be_clickable((By.XPATH, '//*[@id="productDescription"]/div[3]/div[2]/div[1]/a/div[2]/div')))
			# plus_but=driver.find_element_by_xpath('//*[@id="productDescription"]/div[3]/div[2]/div[1]/a/div[2]')
			plus_but.click()
			time.sleep((5) + (random.randint(0, 35) / 35))
			ulta_Ing = driver.find_element_by_xpath('//div[@class="ProductDetail__productContent collapse in"]').text
		except:
			print('Ingredients missing.')
			ulta_Ing = None
		try:
			ulta_Pr = driver.find_element_by_xpath(
				'//*[@id="js-mobileBody"]/div/div/div/div/div/div/section[1]/div[2]/div[1]/div[3]/span').text
		except:
			print('Price missing.')
			ulta_Pr = None
		try:
			ulta_Wgt = driver.find_element_by_xpath(
				'//div[@class="ProductMainSection__itemNumber"]/p[@class="Text Text--body-2 Text--left Text--small"]').text
		except:
			print('Weight missing')
			ulta_Wgt = None
		try:
			ulta_Rev = driver.find_element_by_xpath('//div/span[@class="pr-reco-value"]').text
			ulta_Rcount = driver.find_element_by_xpath('//div/span[@class="pr-snippet-review-count"]').text
		except:
			print('Reviews missing.')
			ulta_Rev = None
			ulta_Rcount = None

		ulta_dict['ulta_Name'] = ulta_Name
		ulta_dict['ulta_Brand'] = ulta_Brand
		ulta_dict['ulta_Ing'] = ulta_Ing
		ulta_dict['ulta_Pr'] = ulta_Pr
		ulta_dict['ulta_Rev'] = ulta_Rev
		ulta_dict['ulta_Wgt'] = ulta_Wgt
		ulta_dict['ulta_Rcount'] = ulta_Rcount
		print('Printing in progress')
		writer.writerow(ulta_dict.values())
		print(ulta_Name)
		print(ulta_Pr)
		print(ulta_Ing)
		print(ulta_Wgt)
	except Exception as e:
		print(e)
		continue
csv_file.close()
driver.quit()
