from selenium import webdriver
#general webdriver
from selenium.common.exceptions import NoSuchElementException
#for when the element isn't there
from selenium.webdriver.common.keys import Keys
#for sending data to forms, like login or group name
from selenium.webdriver.support.ui import WebDriverWait
#for waiting for other stuff to load
from selenium.webdriver.support import expected_conditions as EC
#for waiting for other stuff to load
from selenium.common.exceptions import TimeoutException
#for when waiting for stuff to load takes too long
from selenium.webdriver.common.by import By
#also used when waiting for stuff to load
#bunch of selenium things

from sys import exit
#for when things go wrong
from time import sleep
#for when the system just needs to take a break
import os
#for OS things, like making files and folders
import getpass
#so when you type your password, it isn't visible
import csv
#for getting and storing group data
import signal
#for processing interrupts
import re
#for keyword processing

delay = 4
#if something takes longer than 4 seconds, IMPATIENCE

class bcolors:
    GOODGREEN = '\033[92m'
    WARNYELLOW = '\033[33m'
    SRSYELLOW = '\033[93m'
    BADRED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'
#for formatting pretty text colors

#ctrl+c handler
def signal_handler(signal, frame):
    print(bcolors.WARNYELLOW + 'forcing exit...\nexited.')
    driver.close()
    exit()

#logout stuff
def logout(driver):
    try:
        driver.get('https://www.deviantart.com/settings/sessions')
        logout_button = driver.find_element_by_class_name \
        ('logout-current')
        logout_button.click()
        print(bcolors.GOODGREEN + 'logged out.')
    except:
        print('logout error')
        driver.close()
        exit()
    print('exiting.' + bcolors.ENDC)
    driver.close()
    exit()

#setup stuff
try:
    path = 'data'
    if not (os.path.exists(path)):
        #this folder will hold all program data
        os.makedirs(path)
        #make the data folder
        print(bcolors.WARNYELLOW + 'please load driver into data folder' \
        'and update path: export PATH=$PATH:./data')
        print('please also load CSV files into data folder' + bcolors.ENDC)
        #get the driver into the folder
        exit()
except:
    print(bcolors.BADRED + 'setup error.')
    exit()

uname = ''
pword = ''
kword = ''

while not uname:
    uname = input('enter username: ')

while not pword:
    pword = getpass.getpass('enter password: ')
#both of these should be wiped when the program ends
#neither can be left empty


dev_url = 'http://fav.me/dabhcyw'
#test deviation

do_loop = 1
csv_mode = ''
#will be used to append or overwrite

#file stuff
while(do_loop == 1):
    #make sure, if they accidentally pick a pre-existing file, they
    #don't overwrite it
    fname_input = ''
    while not fname_input:
        #no blank names allowed.
        fname_input = input(bcolors.ENDC + 'enter name for the file: ')
    if(fname_input[-4:] == '.csv'):
        #if they included '.csv'
        fname_input = fname_input[:-4]

    csv_file_name ='./data/'
    csv_file_name += fname_input
    csv_file_name += '.csv'
    #construct the file name

    if os.path.isfile(csv_file_name):
        #the file already exists.
        print(bcolors.WARNYELLOW + \
        'ALERT: file \'', csv_file_name, '\'already exists.\nappend, ' \
        'overwrite, or use a different file name? (a/o/d) ', end='')
        choice = input('')
        if(choice == 'a'):
            #the user wants to append stuff to the file.
            do_loop = 0
            print('entering append mode.' + bcolors.ENDC)
            csv_mode = 'a'
        elif(choice == 'o'):
            #the user wants to overwrite the file.
            print(bcolors.SRSYELLOW + 'WARNING: you will lose ALL DATA in \'',\
            csv_file_name, '\'')
            choice = input('are you sure you want to overwrite? (y/n) ')
            if(str(choice) == 'y'):
                do_loop = 0
                print('WARNING: overwriting file' + bcolors.ENDC)
                csv_mode = 'w'
            else:
                do_loop = 1
    else:
        #file doesn't exist yet. "overwrite" mode
        csv_mode = 'w'
        do_loop = 0

#keyword stuff
kword = input('enter keywords, separated by a space: ')
if kword:
    #they want to use keywords. make them into a list
    #for later use.
    klist = re.sub('[^\w]', ' ', kword).split()
    print(bcolors.GOODGREEN + 'using keywords: ')
    for word in klist:
        #echo their keywords
        print(word + ', ', end='')
    print(bcolors.ENDC, end='')
else:
    #they don't want to use keywords
    klist = []
    print(bcolors.GOODGREEN + 'no keywords in use.' + bcolors.ENDC)
print('')

#webdriver stuff
try:
    print('opening webdriver...')
    driver = webdriver.Chrome()
    #use chrome, coz it's fast
    print(bcolors.GOODGREEN + 'done.' + bcolors.ENDC)
except:
    #the webdriver wasn't found. shut down the program.
    print(bcolors.BADRED +'webdriver error: could not locate web driver.' \
    + bcolors.ENDC)
    print(bcolors.WARNYELLOW + '(try updating path variable: ' \
    'export PATH=$PATH:./data)' + bcolors.ENDC)
    exit()

#login stuff
login_success = False
print('sending login information...')
while(login_success != True):
    #log in. if it doesn't work (i.e. uname, pass entered wrong)
    #loop and do it again

    try:
        driver.get('https://www.deviantart.com/users/login')
        #go to the login page
        login_elem = driver.find_element_by_id \
        ('login_username')
        #go to the username field
        login_elem.clear()
        #clear any existing text out of the username field
        login_elem.send_keys(uname)
        #put in username

        login_elem = driver.find_element_by_id \
        ('login_password')
        #go to password field
        login_elem.clear()
        #clear out any existing text
        login_elem.send_keys(pword)
        #put in password

        login_elem = driver.find_element_by_id \
        ('remember_me')
        #go to "remember me" checkbox
        login_elem.click()
        #uncheck it

        login_elem = driver.find_element_by_class_name \
        ('smbutton')
        #go to login button
        login_elem.click()
        #click it to log in

    except:
        print('login error')
        driver.close()
        exit()

    if(driver.current_url != 'http://www.deviantart.com/browse/all/'):
        #something went wrong with the login; we weren't redirected
        #to the browse page (this happens on successful login)
        try:
            #if they entered an existing uname, go back to the
            #original entry page
            not_me = driver.find_element_by_class_name \
            ('login-not-me')
            #if they entered a valid username
            not_me = not_me.find_element_by_class_name \
            ('small-blue')
            #get the clickable part
            not_me.click()
        except:
            #the uname they entered did not exist, so the 'return to
            #previous page' button did not exist either
            pass
        print('login error. try again.\n')
        uname = input('Enter username: ')
        pword = getpass.getpass('Enter password: ')
    else:
        #we logged in, break the loop
        print(bcolors.GOODGREEN + 'done.' + bcolors.ENDC)
        login_success = True

#navigating to the deviation to submit stuff
try:
    print('navigating to deviation page...')
    driver.get(dev_url)
    #load up a sample deviation to test submissions
    print(bcolors.GOODGREEN + 'done.' + bcolors.ENDC)
except:
    #something went wrong when trying to get the webpage. shut down the
    #driver, and then the program.
    print(bcolors.BADRED + 'driver.get error: could not get webpage')
    print(bcolors.WARNYELLOW + \
    '(did you include \'https://\' in the URL?)' + bcolors.ENDC)
    logout(driver)

#opening the submission box stuff
try:
    print('opening submission box...')
    #see if we can find the submit button
    add_button = driver.find_element_by_id \
    ('groups_links')
    #go to the general location of the button
    add_button = add_button.find_element_by_class_name \
    ('submit_to_groups_link')
    #go to the exact location of the button
    add_button.click()
    #click it
    print(bcolors.GOODGREEN + 'done.' + bcolors.ENDC)
except:
    #the element wasn't found. close the driver and exit
    print(bcolors.BADRED + 'submission box opening error: element not found')
    logout(driver)

#submission box stuff
try:
    print('setting up submission variables...')
    element_present = EC.presence_of_element_located \
    ((By.ID, 'manual_input'))
    WebDriverWait(driver, delay).until(element_present)
    #give the popup a delay of up to four seconds to load
    #wait for manual input button to load, since popup sometimes
    #loads faster than it does

    submit_box = driver.find_element_by_id \
    ('modalspace')
    #find the popup box
    check_button = submit_box.find_element_by_id \
    ('manual_input')
    #find the manual input button
    #we'll reuse this variable later
    check_button.click()
    #click it


    element_present = EC.presence_of_element_located \
    ((By.ID, 'groupname-search'))
    WebDriverWait(driver, delay).until(element_present)
    #give the entry box a delay of up to four seconds to load

    entry_field = submit_box.find_element_by_id \
    ('groupname-search')
    #get the text box
    check_button = submit_box.find_element_by_id \
    ('groupname-check')
    #get the check button
    print(bcolors.GOODGREEN + 'done.')
    print('loading complete.' + bcolors.ENDC)

    #print the message to let users know how this works
    print('\nto include a group, type \'yes\', \'y\',', \
    'or just press enter.')
    print('to omit a group, type anything else.')
    print('to save the current file and exit, type exit at any text entry.')
    print('you can pick up where you left off next time you start.')
except NoSuchElementException:
    print(bcolors.BADRED + 'submission box error: an element was missing.')
    logout(driver)
except TimeoutException:
    print(bcolors.BADRED + \
    'submission box error: something took too long to load.')
    logout(driver)
except:
    print(bcolors.BADRED + 'submission box error: unknown error.')
    logout(driver)

try:
    existing_groups = {}
    #to hold the existing groups. only used in append mode.
    with open(csv_file_name, csv_mode) as newfile:
        #open the to-be-created file
        if(csv_mode != 'a'):
            #write the header if it's not append mode
            fieldnames = ['group_name', 'folder_name', 'folder_value']
            #headers
            writer = csv.DictWriter(newfile, fieldnames=fieldnames)
            #writer
            writer.writeheader()
            #write the header
        writer = csv.writer(newfile, delimiter=',')
        #normal csv writer
        with open('./data/groups.csv') as groupfile:
            #open the group data file
            with open('./data/groups.csv') as tempread:
                #read through existing groups and get a count
                temp_reader = csv.DictReader(tempread)
                total_groups_count = 0
                for row in temp_reader:
                    #add one to the total groups
                    total_groups_count += 1
                #reader should close
            reader = csv.DictReader(groupfile)
            #get a reader for the data file
            existing_groups_count = 0
            if(csv_mode == 'a'):
                #append mode. build a dictionary of existing terms in newfile
                #and compare it to the groups in groupfile. if it exists,
                #skip it.
                with open(csv_file_name) as tempread:
                    #iterate through preexisting groups in the
                    #to-be-appended file
                    temp_reader = csv.DictReader(tempread)
                    for row in temp_reader:
                        #get every already-existing row and ignore it
                        #in the reader
                        existing_groups[str(row['group_name'])] = ''
                        #add it to a dictinary
                        existing_groups_count += 1
                        #keep track of how many groups already added
            print('(', existing_groups_count, 'groups in this list,', \
            total_groups_count, 'groups total,', \
            (total_groups_count - existing_groups_count), 'remain)')
            for row in reader:
                #iterate through all groups

                if((csv_mode == 'a') \
                and (str(row['group_name']) not in existing_groups)) \
                or (csv_mode != 'a'):
                    #if it's append mode and the group's already in the file,
                    #OR if it's not append mode
                    print('')

                    if(existing_groups_count % 10 == 0):
                        print('( group', existing_groups_count, 'of', \
                        total_groups_count, ')')
                    existing_groups_count += 1

                    print('include group:', end='')
                    print(bcolors.BOLD, '', end='')
                    print(row['group_name'], '?', end='')
                    print(bcolors.ENDC, '', end='')
                    include = input('')

                    if(include == 'exit'):
                        #time to exit
                        print('exit in progress...')
                        logout(driver)
                    elif(include == 'a'):
                        #they want to be asked each time
                        writer.writerow([ \
                        row['group_name'], \
                        'ASK', \
                        '-2'])
                        print(bcolors.GOODGREEN + 'will ask.' + \
                        bcolors.ENDC)
                    elif not include or (include == 'y') or (include == 'yes'):
                        #include it
                        #iterate through every row
                        entry_field.clear()
                        #clear any text
                        entry_field.send_keys(row['group_name'])
                        #send it the name retrieved from the groupfile
                        check_button.click()
                        #check and see if it exists

                        try:
                            element_present = EC.element_to_be_clickable \
                            ((By.ID, 'gallery_selection'))
                            WebDriverWait(submit_box, delay) \
                            .until(element_present)
                            #give the folder dropdown menu a delay of up to
                            #four seconds to load

                            select = submit_box.find_element_by_id \
                            ('gallery_selection')
                            #find the selection folder
                            folder_options = select.find_elements_by_tag_name \
                            ('option')
                            #get the folder options
                            folder_num = 0
                            #reset this
                            for option in folder_options:
                                folder_num += 1
                                #for folder number
                                print('folder #', end='')
                                if(folder_num < 10):
                                    print(' ', end='')
                                print(folder_num, ': ', end='')
                                for word in klist:
                                    if(word.lower() in option.text.lower()):
                                        #keyword present
                                        print(bcolors.GOODGREEN, end='')
                                print(option.text + bcolors.ENDC)
                                #print each folder name
                            print('option # a: (ask each time)')
                            print('option # n: (nevermind, don\'t include)')

                            selected = -1
                            while(int(selected) == -1):
                                try:
                                    selected = input \
                                    ('which folder should be used? # ')
                                    if(str(selected) == 'a'):
                                        #they want to be asked
                                        break
                                    elif(str(selected) == 'n'):
                                        #they don't want to include it
                                        break
                                    elif(str(selected) == 'k'):
                                        #add keywords
                                        new_k = input('enter new keywords: ')
                                        if new_k:
                                            new_klist = re.sub \
                                            ('[^\w]', ' ', new_k).split()
                                            klist = klist + new_klist
                                            print(bcolors.GOODGREEN + \
                                            'keywords: ')
                                            for word in klist:
                                                #echo new keywords
                                                print(word + ', ', end='')
                                            print(bcolors.ENDC + '')
                                        else:
                                            #no new keywords added
                                            print(bcolors.GOODGREEN + \
                                            'no keywords added.' \
                                            + bcolors.ENDC)
                                        print('')
                                        selected = -1
                                    elif(str(selected) == 'exit'):
                                        #close it down
                                        print('exit in progress...')
                                        logout(driver)
                                    elif( \
                                    (int(selected) > folder_num) or \
                                    (int(selected) <= 0)):
                                        #they picked something out of bounds
                                        print(bcolors.WARNYELLOW + \
                                        'folder out of bounds:', \
                                        int(selected))
                                        print(bcolors.ENDC, end='')
                                        selected = -1
                                except ValueError:
                                    #they used a symbol that wasn't allowed
                                    print(bcolors.WARNYELLOW + \
                                    'invalid entry:', str(selected) + \
                                    bcolors.ENDC)
                                    selected = -1

                            folder_num = 0
                            if(str(selected) == 'a'):
                                #they want to be asked each time
                                writer.writerow([ \
                                row['group_name'], \
                                'ASK', \
                                '-2'])
                                print(bcolors.GOODGREEN + 'will ask.' + \
                                bcolors.ENDC)
                            elif(str(selected) == 'n'):
                                #htey don't want it included
                                writer.writerow([ \
                                row['group_name'], \
                                'UNUSED', \
                                '-1'])
                                print(bcolors.GOODGREEN + 'group omitted.' + \
                                bcolors.ENDC)
                            else:
                                for option in folder_options:
                                    #look for the folder they specified
                                    folder_num += 1
                                    if(int(folder_num) == int(selected)):
                                        #found the folder
                                        print(bcolors.GOODGREEN + \
                                        'using folder: ', option.text, \
                                        end='')
                                        print(bcolors.ENDC)
                                        #tell the user what they did

                                        writer.writerow([ \
                                        row['group_name'], \
                                        option.text, \
                                        option.get_attribute('value')])
                                        #add the group name, the folder name,
                                        #and the folder value to the csv file

                        except TimeoutException:
                            #for some reason, we couldn't submit to the
                            #group, probably because we didn't have
                            #permission.
                            print(bcolors.WARNYELLOW + \
                            'could not get this group\'s folders.' + \
                            bcolors.ENDC)
                    else:
                        writer.writerow([ \
                        row['group_name'], \
                        'UNUSED', \
                        '-1'])
                        #write a false entry to prevent this from being
                        #used in future appends
                        print(bcolors.GOODGREEN + 'group omitted.' + \
                        bcolors.ENDC)
                        #tell the user what they did
except NoSuchElementException:
    print(bcolors.BADRED + 'csv writer error: an element was missing')
    logout(driver)
#except:
#    print(bcolors.BADRED + 'csv writer error: unknown error.')
#    print('(WARNING: program bug detected. please tell paper.)')
#    logout(driver)

#commented out because logging out threw unknown errors when this was active,
#but threw nothing when it was not.

print(bcolors.GOODGREEN + '\nall groups done.\nlogging out...')
logout(driver)
