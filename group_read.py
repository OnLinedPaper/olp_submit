#navigates to userpage of deviant and reads every group they're part
#of, condensing it into one csv file groups.csv

from selenium import webdriver
#general webdriver
from sys import exit
#for when things go wrong
from time import sleep
#for when the system just needs to take a break
import os
#for OS things, like making files and folders
import csv
#for csv things
import signal
#for processing interrupts

def signal_handler(signal, frame):
    print('exiting.')
    driver.close()
    exit()

#setup stuff
try:
    path = 'data'
    if not (os.path.exists(path)):
        #this folder will hold all program data
        os.makedirs(path)
        #make the data folder
except:
    print('setup error.')
    exit()

uname = input('Enter username: ')

#webdriver stuff
try:
    driver = webdriver.Chrome()
    #use chrome, coz it's fast
except:
    #the webdriver wasn't found. shut down the program.
    print('webdriver error: could not locate web driver.')
    print('(linux users, try updating path variable: \
    export PATH=$PATH:./data)')
    exit()

offset = 0;
count = 0;

print('now loading groups into ./data/groups.txt')

#loading the groups stuff
with open('./data/groups.csv', 'w') as csvfile:
    fieldnames = ['group_name', 'folder_name', 'folder_value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    while(1):
        try:
            target = "https://"
            target += uname
            target += ".deviantart.com/modals/mygroups?offset="
            target += str(offset)
            #build the group path

            driver.get(target)
        except:
            print('something went wrong when trying to get the group list.')
            #but if something went wrong when building a string, you've
            #got bigger problems
            driver.close()
            exit()

        try:
            all_groups_on_page = driver.find_elements_by_class_name \
            ('mygroup')
            if(len(all_groups_on_page) == 0):
                #we hit a page with no groups, so we went through them all.
                #break the loop.
                print('all groups loaded. total:', count, '        ')
                break
            #get every group of 'mygroup' class

            for group in all_groups_on_page:
                #iterate through every group
                url = group.find_element_by_tag_name \
                ('a')
                #go to the link
                tosplit = url.get_attribute('href')
                #get the hyperlink
                tosplit = tosplit[7:]
                #remove 'http://'
                tosplit = tosplit[:-16]
                #remove '.deviantart.com/'
                #leave nothing but the name
                count += 1;
                print(' added ', count, 'groups (', tosplit, \
                ')                ', end='\r', flush=True)

                writer.writerow \
                ({'group_name': tosplit, 'folder_name': "ASK", \
                'folder_value': '-2'})
                #write it to the file

        except:
            print('something went wrong when loading groups.')
            csvfile.close()
            driver.close()
            exit()
        offset += 100

csvfile.close()
driver.close()
exit()
