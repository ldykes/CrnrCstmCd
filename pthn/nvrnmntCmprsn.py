import os
import shutil
import pandas as pd
import win32com.client as win32
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

'''GLOBALS'''
print("GLOBALS")
driver = webdriver.Chrome(executable_path=r"")#path to webdriver
src_path = r""#path for file dl
dst_path = r""#same as above
wrkngPth = r""#same but + x for xls to xlsx conversion
flExsts = False
print("Finishing GLOBALS")
'''FUNCTIONS'''
# login to distributions.cerner.com
'''need to run browser in the background if at all possible'''
print("login to distributions.cerner.com")
driver.get()#Installation History URL
driver.find_element(By.ID, "react521395710").click()
driver.find_element(By.ID, "authUsername").send_keys("")#username
driver.find_element(By.ID, "authPassword").send_keys("" + Keys.ENTER)#password
print("Finishing login to distributions.cerner.com")
# wait for page to generate
print("wait for page to generate")
driver.implicitly_wait(10)
print("finishing wait for page to generate")
# generate excel package file
print("generate excel package file")
driver.find_element(By.CSS_SELECTOR, ".select__value-container").click()
driver.find_element(By.ID, "react-select-2-option-0-1").click()
driver.find_element(By.ID, "react-select-2-option-0-3").click()
driver.find_element(By.CSS_SELECTOR, ".select__dropdown-indicator > .css-8mmkcg").click()
driver.find_element(By.ID, "cmdExport").click()
print("finishing generate excel package file")
# check for Excel file
print("check for Excel file")
while not flExsts:

    driver.implicitly_wait(10)

    if Path(src_path).is_file():
        flExsts = True
print("finishing check for Excel file")
# move Excel file to python folder
print("move Excel file to python folder")

driver.implicitly_wait(10)

shutil.move(src_path, dst_path)
print("finishing move Excel file to python folder")
# convert xls to xlsx
print("convert xls to xlsx")
print("opening workbook")
wb = win32.gencache.EnsureDispatch('Excel.Application').Workbooks.Open(dst_path)
print("finishing opening workbook")
wb.SaveAs(dst_path + "x", FileFormat=51)  # FileFormat = 51 is for .xlsx extension
wb.Close()
win32.gencache.EnsureDispatch('Excel.Application').Application.Quit()
os.remove(dst_path)
print("finishing convert xls to xlsx")
# compare packages in environments
print("compare packages in environments")
nstlltnHst = pd.read_excel(wrkngPth, "Installation_history_data_ex", header=12)
cert = nstlltnHst.query('Environment == "C523"')[['Package #', 'Version']]
prod = nstlltnHst.query('Environment == "P523"')[['Package #', 'Version']]
ndVldtn = cert.merge(prod.drop_duplicates(), on=['Package #', 'Version'], how='left', indicator=True)
ndVldtn = ndVldtn.query('_merge == "left_only"')[['Package #', 'Version']]
print(ndVldtn)
print("finishing compare packages in environments")
# remove file once done working with it
print("remove file once done working with it")
os.remove(wrkngPth)
print("finishing remove file once done working with it")
