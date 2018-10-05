#-*- coding: utf-8 -*-

from __future__ import print_function
from selenium import webdriver
import os
import zipfile
import time


import numpy

tmp_dir = '/tmp'
full_url = 'http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=293'   # Download file by selecting all fields

if not os.path.isdir(tmp_dir):
    os.mkdir(tmp_dir)
import glob

def download_one(month, year):
   """
   Download a single year_month's flights. It is not easy to identify where the files are located, so this function
   mimics a user filling the form, selecting year and month as well as all variables, and clicking download.
   :param month: integer
   :param year: integer
   :return: a single renamed csv file
   """
   end_name = "US_Segments_%s-%s.csv" % (month, year)

   # Set chrome options and reach the website
   # options = webdriver.ChromeOptions()
   # options.add_experimental_option("prefs", {
   #     "download.default_directory": tmp_dir,
   #     "download.prompt_for_download": False,
   # })
   # driver = webdriver.Chrome(chrome_options=options)

   #options = webdriver.FirefoxOptions()
   # options.set_preference("prefs", {
   #     "download.default_directory": tmp_dir,
   #     "download.prompt_for_download": False,
   # })

   options = webdriver.FirefoxProfile()
   options.set_preference("browser.download.folderList", 2)
   options.set_preference("browser.download.dir",os.getcwd()+'\\'+'temp')
   options.set_preference("browser.helperApps.alwaysAsk.force", False);
   options.set_preference("browser.download.manager.showWhenStarting", False)
   options.set_preference("browser.helperApps.neverAsk.saveToDisk","application/x-zip-compressed")

   driver = webdriver.Firefox(firefox_profile=options)
   driver.get(full_url)
   assert "OST_R | BTS | Transtats" in driver.title

   # Select the demanded year and month
   driver.find_element_by_xpath("//select[@id='XYEAR']/option[@value=%s]" % year).click()
   if type(month) == 'str':
       driver.find_element_by_xpath("//select[@id='FREQUENCY']/option[@value=%s]" % month).click()
   else:
       driver.find_element_by_xpath("//select[@id='FREQUENCY']/option[@value='" + month.lstrip() + "']").click()
   # Click the "select all variables checkbox", then click download
   """
   It could be useful to select only the required variables instead of all of them, but
   the difference in filesize isn't very important, so I just identified the one button.
   """
   driver.find_element_by_name('AllVars').click()
   driver.find_element_by_name("Download").click()

   # Wait for file to be downloaded
   time.sleep(50)
   while glob.glob(os.getcwd() + "/" + "temp/"+'*.part'):
           time.sleep(50)
   time.sleep(10)
   driver.close()
       #time.sleep(50)


   #Identify downloaded zip file, then unzip its content and delete zip file
   zip_name = max([os.getcwd() + "/" + "temp/" + f for f in os.listdir("temp")], key=os.path.getctime)
   zip_ref = zipfile.ZipFile(zip_name, 'r')
   zip_ref.extractall(os.getcwd() + "\\" + "temp")
   zip_ref.close()
   os.remove(zip_name)

   # Identify csv file name, and rename to "US_Segment_month-year.csv"
   csv_name = max([os.getcwd() + "/" + "temp/" + f for f in os.listdir(os.getcwd() + "/" + "temp/")],
                  key=os.path.getctime)
   os.rename(os.path.join(os.getcwd() + "/" + "temp/", csv_name), os.path.join(os.getcwd() + "/" + "temp/", end_name))
   print("%s downloaded", end_name)
   end_name = ''

   return end_name


def robot_download(month, year):
   """
   Depending on whether month and/or year are single or multiple values, iterate to download the relevant files
   :param month: integer or tuple of integers
   :param year: integer or tuple of integers
   :return: list of downloaded csv files
   """
   csv_files = []
   if  isinstance(month, int) and  isinstance(year, int):
           csv_files.append(download_one(month, year))
   elif isinstance(month, str) and  isinstance(year, str):
       csv_files.append(download_one(month, year))
   elif isinstance(month, str) and isinstance(year, list):
       for y in year:
           csv_files.append(download_one(month, y))
   else:
       if isinstance(month, list) and isinstance(year, list):
           for y in year:
               for m in month:
                   csv_files.append(download_one(m, y))
       else:
           if isinstance(month, list):
               for m in month:
                   csv_files.append(download_one(m, year))
           else:
               for y in year:
                   csv_files.append(download_one(month, y))
   return csv_files



def main():
   print('Starting to get data from Bureau of Transportation Statistics')
   year = raw_input("Enter year(s) to download (separated by a comma")
   if ',' in year:
       print ("test")
       year = year.split(',')
   if type(year) == 'int':
       year.strip()
   month = raw_input("Enter month number(s) (separated by a comma")
   print (type(month))

   if ',' in month:
        month = month.split(',')
        csv_files = robot_download(month, year)
   else:
       csv_files = robot_download(month.strip(), year)


if __name__ == '__main__':
    main()
