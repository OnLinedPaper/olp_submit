import traceback
import sys
from selenium import webdriver
#general webdriver
import csv
#print(1/0)

with open('./data/text.csv', 'a') as newfile:
    #write the header if it's not append mode
    fieldnames = ['group_name', 'folder_name', 'folder_value']
    #headers
    writer = csv.DictWriter(newfile, fieldnames=fieldnames)
    #writer
    writer.writeheader()
    #write the header

with open('./data/test.csv', 'a') as newfile:
    #write the header if it's not append mode
    fieldnames = ['group_name', 'folder_name', 'folder_value']
    #headers
    writer = csv.DictWriter(newfile, fieldnames=fieldnames)
    #writer
    writer.writeheader()
    #write the header
