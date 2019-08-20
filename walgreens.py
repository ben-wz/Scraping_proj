from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # explicit waits
from selenium.webdriver.support import expected_conditions as EC  # expected conditions
from functools import reduce

import time  # sleeptime
import datetime  # for date
import re
import random


# For csv file names
def reduce_concat(x, sep=""):
    return reduce(lambda x, y: str(x) + sep + str(y), x)


def paste(*lists, sep=" ", collapse=None):
    result = map(lambda x: reduce_concat(x, sep=sep), zip(*lists))
    if collapse is not None:
        return reduce_concat(result, sep=collapse)
    return list(result)


dateNow = datetime.datetime.now()
# driver = webdriver.Chrome()
chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images': 2}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chromeOptions)
driver.get("https://www.walgreens.com/store/store/category/productlist.jsp?N=360453&Eon=360453")  # start url

import csv

filename = paste(['walG_cosFace'], [dateNow.year], ['-'], [dateNow.month], ['-'], [dateNow.day], ['.csv'], sep='')
filename = ''.join(filename)
csv_file = open(filename, 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

index = 1
cos_LinksAll = []
while True:
    if index > 33:  # change to length of review list
        break
    try:
        print('Goin thru page ' + str(index))
        index += 1
        time.sleep((3) + (random.randint(0, 500) / 500))
        cos_List = (driver.find_elements_by_xpath('//*[contains(@id, "title-secondary-0compare")]'))
        cos_Links = [i.get_attribute('href') for i in cos_List]
        cos_LinksAll.extend(cos_Links)

        # next button
        waiTTT = WebDriverWait(driver, 10)
        # next_but=waiTTT.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="icon icon__arrow-right"]')))
        next_but = waiTTT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="omni-next-click"]/span')))
        next_but.click()

    except Exception as e:
        print(e)
        continue
print(cos_LinksAll)  # works till here :D
for linkK in cos_LinksAll:
    # Use a dictionary
    cosm_dict = {}
    driver.get(linkK)
    print(linkK)

    try:  # i think this sleep is for loading the webpage
        time.sleep((1.5) + (random.randint(0, 222) / 222))

        try:
            cosm_Name = driver.find_element_by_xpath('//span[@id="productTitle"]').text
        except:
            print('Name missing.')
            cosm_Name = None
        try:
            cosm_Ctry = driver.find_element_by_xpath('//*[text()[contains(.,"Made in")]]').text
        except:
            print('Country missing.')
            cosm_Ctry = None
        try:
            cosm_Ing = driver.find_element_by_xpath(
                '//div[@class="wag-accordion-tab-content" and @id="Description-2"]//div/div/div/div/div/span').text
        except:
            print('Ingredients missing.')
            cosm_Ing = None
        try:
            cosm_Wgt = driver.find_element_by_xpath('//*[@id="productSizeCount"]').text
        except:
            print('Weight missing.')
            cosm_Wgt = None
        try:
            cosm_Dol = driver.find_element_by_xpath('//*[@id="regular-price"]/span/span').text
            cosm_Cen = driver.find_element_by_xpath('//*[@id="regular-price"]/span/sup[2]').text
            cosm_Pr = float(cosm_Dol + '.' + cosm_Cen)
        except:
            print('Price missing.')
            cosm_Pr = None
        try:
            cosm_Rev = float(driver.find_element_by_xpath('//span[@itemprop="ratingValue"]').text)
            cosm_Rcount = float(driver.find_element_by_xpath('//span[@itemprop="reviewCount"]').text)
        except:
            print('Reviews missing.')
            cosm_Rev = None

        cosm_dict['cosm_Name'] = cosm_Name
        cosm_dict['cosm_Ctry'] = cosm_Ctry
        cosm_dict['cosm_Ing'] = cosm_Ing
        cosm_dict['cosm_Pr'] = cosm_Pr
        cosm_dict['cosm_Rev'] = cosm_Rev
        cosm_dict['cosm_Rcount'] = cosm_Rcount
        cosm_dict['cosm_Wgt'] = cosm_Wgt
        print('Printing in progress')
        writer.writerow(cosm_dict.values())
        print(cosm_Name)

    except Exception as e:
        print(e)
        continue

csv_file.close()
driver.close()