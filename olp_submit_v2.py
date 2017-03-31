from selenium import webdriver
#general webdriver
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
import re
#for keyword processing

delay = 4
long_delay = 16
#if something takes longer than 4 seconds, IMPATIENCE

#for formatting pretty text colors
class bcolors:
    GOODGREEN = '\033[92m'
    WARNYELLOW = '\033[33m'
    SRSYELLOW = '\033[93m'
    BADRED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

#logout stuff
def logout(driver):
    try:
        driver.get('https://www.deviantart.com/settings/sessions')
        logout_button = driver.find_element_by_class_name \
        ('logout-current')
        logout_button.click()
        print(bcolors.GOODGREEN + 'logged out.')
    except:
        print(bcolors.BADRED + 'logout error')
        driver.close()
        exit()
    print('exiting.' + bcolors.ENDC)
    driver.close()
    exit()

#setup stuff
try:
    print('running setup tasks...')
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
dpage = ''

do_later = {}
#will hold anything that needs to be dealt with

while not uname:
    uname = input('Enter username: ')

while not pword:
    pword = getpass.getpass('Enter password: ')
#both of these should be wiped when the program ends
#neither can be left empty

while not dpage:
    dpage = input('Paste the deviation\'s URL: ')


csv_file_name = ''
while not os.path.isfile(csv_file_name):
    #make sure the specified file is real
    fname_input = ''
    while not fname_input:
        fname_input = input('enter name of file: ')
    if(fname_input[-4:] == '.csv'):
        #if they included '.csv'
        fname_input = fname_input[:-4]

    csv_file_name ='./data/'
    csv_file_name += fname_input
    csv_file_name += '.csv'
    #construct the file name

if not os.path.isfile('./data/.replace.csv'):
    #make the hidden "replace" folder
    with open('./data/.replace.csv', 'w') as replace:
        writer = csv.writer(replace)
        writer.writerow(['group_name','folder_name','folder_value'])
else:
    os.remove('./data/.replace.csv')
    #remove old replace file and make a new one
    with open('./data/.replace.csv', 'w') as replace:
        writer = csv.writer(replace)
        writer.writerow(['group_name','folder_name','folder_value'])

#keyword stuff
kword = input('enter keywords, separated by a space: ')
if kword:
    #they want to use keywords. make them into a list
    #for later use.
    klist = re.sub('[^\w]', ' ', kword).split()
    print(bcolors.GOODGREEN + 'using keywords: ')
    for word in klist:
        #echo their keywords
        print(word)
    print(bcolors.ENDC, end='')
else:
    #they don't want to use keywords
    klist = []
    print(bcolors.GOODGREEN + 'no keywords in use.' + bcolors.ENDC)
print('')

#webdriver stuff
try:
    print('activating webdriver...')
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
print('logging in...')
login_success = False
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
        print(bcolors.BADRED + 'login error')
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
        login_success = True
print(bcolors.GOODGREEN + 'done.' + bcolors.ENDC)

#navigating to the deviation to submit stuff
try:
    print('navigating to target deviation...')
    driver.get(dpage)
    print(bcolors.GOODGREEN + 'done.' + bcolors.ENDC)
    #load up the webpage
except:
    #something went wrong when trying to get the webpage. shut down the
    #driver, and then the program.
    print(bcolors.BADRED + 'driver.get error: could not get webpage')
    print(bcolors.WARNYELLOW + '(did you include \'https://\' in the URL?)')
    logout(driver)

#opening the submission box stuff
try:
    print('opening submisson box...')
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
    print('opening manual input...')
    element_present = EC.presence_of_element_located \
    ((By.ID, 'manual_input'))
    WebDriverWait(driver, delay).until(element_present)
    #give the popup a delay of up to four seconds to load

    submit_box = driver.find_element_by_id \
    ('modalspace')
    #find the popup box
    check_button = submit_box.find_element_by_id \
    ('manual_input')
    #find the manual input button
    #we'll reuse this variable later
    check_button.click()
    #click it
    print(bcolors.GOODGREEN + 'done.' + bcolors.ENDC)

    print('establishing submission variables...')
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
    print('setup tasks complete.' + bcolors.ENDC)

    with open(csv_file_name) as csvfile:
        #the file containing group info
        reader = csv.DictReader(csvfile)
        #get a reader
        success_subs = 0
        ask_subs = 0
        error_subs = 0
        failure_subs = 0
        #tracking data: successes, asks, errors, failures
        for row in reader:
            #iterate through all rows in the input file.
            #if it's a -1, ignore it.
            #if it's a -2, get the folder names to deal with later.
            if(row['folder_value'] is None):
                #empty value
                print(bcolors.SRSYELLOW, end='')
                print('WARNING: csv file corruption detected. group:', end='')
                print(row['group_name'], bcolors.ENDC)
            if(int(row['folder_value']) == -1):
                #it's not used.
                pass
            else:
                entry_field.clear()
                #clear any text
                entry_field.send_keys(row['group_name'])
                #send it the name
                check_button.click()
                #check and see if it exists

                sleep(1)

                submit_status = submit_box \
                .find_element_by_class_name \
                ('error_message')
                #find the error message
                if(submit_status.get_attribute('style') == \
                'display: none;'):
                    #deviation not yet part of group

                    element_present = EC.element_to_be_clickable \
                    ((By.ID, 'gallery_selection'))
                    WebDriverWait(submit_box, long_delay).until(element_present)
                    #give the folder dropdown menu a delay of up to four seconds
                    #to load

                    select = submit_box.find_element_by_id \
                    ('gallery_selection')
                    #find the selection folder
                    folder_options = select.find_elements_by_tag_name \
                    ('option')
                    #get the folder options

                    if(int(row['folder_value']) == -2):
                        #the user needs to be asked.
                        #save this folder and deal with it later.
                        do_later[str(row['group_name'])] = 'ask'
                        #add it to a dict to deal with it later
                        print(bcolors.GOODGREEN, end='')
                        print('storing group: ', row['group_name'], \
                        '\n(asking after automated submissions finish.)\n\n', \
                        end='')
                        print(bcolors.ENDC, end='')
                        ask_subs += 1
                    else:
                        #submit it automatically.
                        success = -1
                        #if the folder was removed, this will catch it
                        for option in folder_options:
                            if(option.get_attribute('value') == \
                            str(row['folder_value'])):
                                #the folder's id matches where we want to submit
                                success = 0
                                option.click()

                                submit_button = submit_box \
                                .find_element_by_class_name \
                                ('submit')
                                #find the submit button
                                submit_button.click()
                                #click it to submit

                                sleep(1)
                                #give it a second to go through

                                submit_status = submit_box \
                                .find_element_by_class_name \
                                ('error_message')
                                #find the error message
                                if(submit_status.get_attribute('style') == \
                                'display: none;'):
                                    #see if the error is displaying.
                                    #if not, a succes message is
                                    #displaying (hopefully)

                                    submit_status = submit_box \
                                    .find_element_by_class_name \
                                    ('success_message')
                                    #get the success message
                                    #this should be displaying if an error
                                    #message is not

                                    print(bcolors.GOODGREEN + 'successful:')
                                    print('group: ', row['group_name'], \
                                    '\nfolder:', row['folder_name'], \
                                    '\nmessage: \'', submit_status \
                                    .find_element_by_tag_name \
                                    ('span').text, '\'')
                                    print('' + bcolors.ENDC)
                                    #group: group
                                    #folder: folder
                                    #message: whatever the message was
                                    success_subs += 1

                                else:
                                    #there was an error
                                    do_later[str(row['group_name'])] \
                                    = 'error'
                                    #deal with it later

                                    print(bcolors.WARNYELLOW + 'unsuccessful:')
                                    print('group: ', row['group_name'], \
                                    '\nfolder:', row['folder_name'], \
                                    '\nmessage: \'', submit_status \
                                    .find_element_by_tag_name \
                                    ('span').text, '\'')
                                    print('' + bcolors.ENDC)
                                    #group: group
                                    #folder: folder
                                    #message: whatever the message was
                                    error_subs += 1
                        if(success == -1):
                            #the folder was not found
                            do_later[str(row['group_name'])] \
                            = 'error'
                            #deal with it later

                            print(bcolors.WARNYELLOW + 'unsuccessful:')
                            print('group: ', row['group_name'], \
                            '\nfolder:', row['folder_name'], \
                            '\n(folder not found)')
                            print('' + bcolors.ENDC)
                            #group: group
                            #folder: folder
                            #message: whatever the message was
                            error_subs += 1
                else:
                    #it was either already in the group, or it can't
                    #be submitted there.
                    print(bcolors.WARNYELLOW + 'unsuccessful:')
                    print('group: ', row['group_name'], \
                    '\nfolder:', row['folder_name'], \
                    '\nmessage: \'', submit_status \
                    .find_element_by_tag_name \
                    ('span').text, '\'')
                    print('' + bcolors.ENDC)
                    failure_subs += 1
except TimeoutException:
    #the element wasn't found. close the driver and exit
    print(bcolors.BADRED + \
    'automated submission error: something took too long to load.')
    driver.close()
    exit()
#except:
#    print(bcolors.BADRED + 'automated submission error: unknown error.')
#    print('(WARNING: program bug detected. please tell paper.)')
#    driver.close()
#    exit()

#closed the file at this point.

print(bcolors.GOODGREEN + 'automated submissions complete.' + bcolors.ENDC)
print(success_subs, 'successesfully submitted')
print(ask_subs, 'to be asked about')
print(error_subs, 'encountered errors')
print(failure_subs, 'could not be submitted')

manual_subs = 0
#track manual sub list

try:
    #deal with asks and errors
    with open(csv_file_name) as csvfile:
        #reopen the file and read through it to deal with the others
        reader = csv.DictReader(csvfile)
        #get a reader
        for row in reader:
            if(str(row['group_name']) in do_later):
                manual_subs += 1
                if(manual_subs % 10 == 0):
                    #sanity check to see how many are left
                    print('(group', manual_subs, 'of', \
                    (ask_subs + error_subs), ')')
                success = -1
                while(success == -1):
                    #this needs to be dealt with.
                    entry_field.clear()
                    #clear any text
                    entry_field.send_keys(row['group_name'])
                    #send the folder
                    check_button.click()
                    try:
                        element_present = EC.element_to_be_clickable \
                        ((By.ID, 'gallery_selection'))
                        WebDriverWait(submit_box, long_delay) \
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
                        print('\nfor group:', end='')
                        print(bcolors.BOLD, '', end='')
                        print(row['group_name'], end='')
                        print(bcolors.ENDC, '')
                        #ask what the user wants

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
                        print('option # i: (ignore the group this time)')
                        print('option # s: (stop using this group)')

                        selected = -1
                        while(int(selected) == -1):
                            try:
                                selected = input \
                                ('which folder should be used? # ')
                                if(str(selected) == 'i'):
                                    #they want to ignore it
                                    success = 0
                                    break
                                elif(str(selected) == 'k'):
                                    #add keywords
                                    new_k = input('enter new keywords: ')
                                    if new_k:
                                        new_klist = re.sub \
                                        ('[^\w]', ' ', new_k).split()
                                        klist = klist+new_klist
                                        print(bcolors.GOODGREEN + \
                                        'keywords: ')
                                        for word in klist:
                                            #echo new keywords
                                            print(word + ', ', end='')
                                        print(bcolors.ENDC)
                                        selected = -1
                                elif(str(selected) == 's'):
                                    #they want to remove it
                                    success = 0
                                    break
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

                        if(str(selected) == 'i'):
                            #they want to ignore it
                            print(bcolors.GOODGREEN + 'ignored.' + \
                            bcolors.ENDC)
                            pass
                        elif(str(selected) == 's'):
                            #set the group to UNUSED
                            with open ('./data/.replace.csv', 'a') \
                            as replace:
                                r_writer = csv.writer(replace)
                                r_writer.writerow([ \
                                row['group_name'], \
                                'UNUSED', \
                                '-1'])
                                #edit the csv file
                                #csv file
                            print(bcolors.WARNYELLOW + 'removed.' + \
                            bcolors.ENDC)
                            success = 0
                        else:
                            #they want to use it
                            folder_num = 0
                            for option in folder_options:
                                #look for the folder they specified
                                folder_num += 1
                                if(int(folder_num) == int(selected)):
                                    #found the folder
                                    temp_fname = option.text
                                    temp_fval = \
                                    option.get_attribute('value')
                                    #for updating
                                    option.click()

                                    submit_button = submit_box \
                                    .find_element_by_class_name \
                                    ('submit')
                                    #find the submit button
                                    submit_button.click()
                                    #click it to submit

                                    sleep(1)
                                    #give it a second to go through

                                    submit_status = submit_box \
                                    .find_element_by_class_name \
                                    ('error_message')
                                    #find the error message
                                    if(submit_status.get_attribute('style') \
                                    == 'display: none;'):
                                        #see if the error is displaying.
                                        #if not, a succes message is
                                        #displaying (hopefully)

                                        submit_status = submit_box \
                                        .find_element_by_class_name \
                                        ('success_message')
                                        #get the success message
                                        #this should be displaying if an error
                                        #message is not

                                        print(bcolors.GOODGREEN + \
                                        'successful:')
                                        print('group: ', row['group_name'], \
                                        '\nfolder:', temp_fname, \
                                        '\nmessage: \'', submit_status \
                                        .find_element_by_tag_name \
                                        ('span').text, '\'')
                                        print('' + bcolors.ENDC)
                                        #group: group
                                        #folder: folder
                                        #message: whatever the message was

                                        if(int(row['folder_value']) != -2):
                                            #it was an error
                                            print \
                                            ('do you want to make folder:', \
                                            temp_fname, \
                                            '\nthe default folder for group:', \
                                            row['group_name'], \
                                            '? (y/n) ', end='')
                                            replace_it = input('')
                                            if(str(replace_it) == 'y'):
                                                with open \
                                                ('./data/.replace.csv', 'a') \
                                                as replace:
                                                    r_writer = csv.writer( \
                                                    replace)
                                                    r_writer.writerow([ \
                                                    row['group_name'], \
                                                    temp_fname, \
                                                    option.get_attribute \
                                                    ('value')])
                                                    #write a replacement
                                                    #csv file

                                        success = 0
                                        #break the loop and go to the next
                                        #thing that needs to be addressed

                                    else:
                                        print(bcolors.SRSYELLOW + \
                                        'unsuccessful:')
                                        print('group: ', row['group_name'], \
                                        '\nfolder:', row['folder_name'], \
                                        '\nmessage: \'', submit_status \
                                        .find_element_by_tag_name \
                                        ('span').text, '\'')
                                        print('' + bcolors.ENDC)
                                        #group: group
                                        #folder: folder
                                        #message: whatever the message was

                    except TimeoutException:
                        #for some reason, we couldn't submit to the
                        #group, probably because we didn't have
                        #permission.
                        print(bcolors.WARNYELLOW + \
                        'could not get this group\'s folders.' + \
                        bcolors.ENDC)
                        success = 0


except TimeoutException:
    #the element wasn't found. close the driver and exit
    print(bcolors.BADRED + \
    'manual submission error: something took too long to load.')
    driver.close()
    exit()
except:
    print(bcolors.BADRED + 'manual submission error: unknown error.')
    print('(WARNING: program bug detected. please tell paper.)')
    driver.close()
    exit()

print(bcolors.GOODGREEN + '\nall groups processed.')
print('logging out...')
#WE MADE IT

logout(driver)

driver.close()
#shut down the driver
exit()
#we're done here
