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
import traceback
#for error logging
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
import datetime
#misc use, mostly for error logging

global delay
delay = 4
#if something takes longer than 4 seconds, something is up
global fieldnames
fieldnames = ['group_name', 'folder_name', 'folder_value']
#these will be used by CSV files

#==============================================================================
#class and function definitions

#------------------------------------------------------------------------------
#for formatting pretty text colors
class bcolors:
    GOODGREEN = '\033[92m'
    WARNYELLOW = '\033[33m'
    SRSYELLOW = '\033[93m'
    BADRED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

#------------------------------------------------------------------------------
#error logging function
#takes a string and prints a traceback to an error file, as well as the string
#to stdout
def log_error(e):
    try:
        with open('./data/.errorlog.txt', 'a') as elog:
            #write error to file
            errordate = str(datetime.datetime.now()) + '\n\n'
            elog.write(errordate)
            elog.write(traceback.format_exc())

        #print the error for the user to see
        print(bcolors.BADRED, end='')
        print('error type:\t', type(e), '\n\"', e, '\"\n', end='')
        print(bcolors.ENDC, end='')

    except Exception as e:
        #the error logger had an error? that's not good.
        print(bcolors.BADRED + 'log_error error' + bcolors.ENDC)
        print(type(e))
        print(e)

#------------------------------------------------------------------------------
#setup function
#takes no arguments and sets up the external data
def setup():
    try:
        #ensure the "data" folder exists
        if not (os.path.exists('data')):
            #data folder does not exist
            #probably means csv folders also don't exist
            os.makedirs('data')
            print(bcolors.WARNYELLOW + \
            'please load CSV files into data folder')
            exit()

    except Exception as e:
        #i don't anticipate an error ever occuring here
        print(bcolors.BADRED, end='')
        print('setup error: error while checking for data folder.', end='')
        print(type(e), '\t\"', e, '\"', end='')
        print(bcolors.ENDC)
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up error log file
        errorlog = './data/.errorlog.txt'
        #store name for easier use
        if os.path.isfile(errorlog):
            #if there's an error log, delete it
            os.remove(errorlog)
        with open(errorlog, 'a'):
            #create a blank file for the errorlog
            pass

    except Exception as e:
        #if an error occurs here, it's probably something to do with the
        #error log. this is the only except function that won't call
        #log_error, since it would try to reference a bad file.
        print(bcolors.BADRED, end='')
        print('setup error: error while setting up errorlog file.', end='')
        print(type(e), '\t\"', e, '\"', end='')
        print(bcolors.ENDC)
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up the replacement file
        replacefile = './data/.replace.csv'
        #store the name for easier use
        if os.path.isfile(replacefile):
            #if there's a preexisting replace file
            os.remove(replacefile)
        with open(replacefile, 'a') as newfile:
            #create a file for the replace csv
            writer = csv.DictWriter(newfile, fieldnames=fieldnames)
            #writer
            writer.writeheader()
            #write the header

    except Exception as e:
        print(bcolors.BADRED + \
        'setup error: error while setting up replace file.' +
        bcolors.ENDC)
        log_error(e)
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up the "deal with this later" file
        laterfile = './data/.later.csv'
        #store the name for easier use
        if os.path.isfile(laterfile):
            #if a file already exists
            pass
        else:
            #we need to create a file
            with open(laterfile, 'a') as newfile:
                #create a file for the later csv
                writer = csv.DictWriter(newfile, fieldnames=fieldnames)
                #writer
                writer.writeheader()
                #write the header

    except Exception as e:
        print(bcolors.BADRED + \
        'setup error: error while setting up error handling file.' +
        bcolors.ENDC)
        log_error(e)
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        if not os.path.isfile('./data/chromedriver') \
        and not os.path.isfile('C:\Windows\chromedriver.exe'):
            #the driver isn't installed
            print(bcolors.WARNYELLOW, end='')
            print('alert: chromedriver is not installed.' + bcolors.ENDC)
            exit()

    except Exception as e:
        print(bcolors.BADRED + 'setup error: error while looking for driver' \
        + bcolors.ENDC)
        log_error(e)
        exit()

#------------------------------------------------------------------------------
#csv file function
#takes nothing and returns a string containing the csv file
def get_csv_file():
    try:
        csv_file_name = ''
        #clear csv_file_name
        while not os.path.isfile(csv_file_name):
            #assert that the entered csv file exists
            fname_input = ''
            #this will hold the name the user wants to use
            while not fname_input:
                #loop until a non-empty fname is entered
                fname_input = input('enter name of file: ')
                if(fname_input[-4:] == '.csv'):
                    #they included '.csv' in the name
                    fname_input = fname_input[:-4]
                    #take out '.csv'
            csv_file_name = './data/'
            csv_file_name += fname_input
            csv_file_name += '.csv'
            #construct the file name
            #the while loop will now check to make sure it exists
            return csv_file_name

    except Exception as e:
        #the driver is not open
        print(bcolors.BADRED + 'get_csv_file error' + bcolors.ENDC)
        log_error(e)
        exit()

#------------------------------------------------------------------------------
#webdriver function
#takes no arguments, and returns an active webdriver
def open_webdriver():
    try:
        drv = webdriver.Chrome()
        return drv

    except Exception as e:
        #the driver is not open
        print(bcolors.BADRED + 'open_webdriver error' + bcolors.ENDC)
        log_error(e)
        exit()

#==============================================================================
#BEYOND THIS POINT, THE WEBDRIVER IS ACTIVE.
#ERROR HANDLERS MUST CLOSE THE DRIVER BEFORE EXITING THE PROGRAM.
#==============================================================================

#------------------------------------------------------------------------------
#username function
#takes no arguments and returns a string with the username in it
def get_username():
    try:
        uname = ''
        #clear uname
        while not uname:
            #loop until a non-empty uname is entered
            uname = input('enter username: ')
        return uname

    except Exception as e:
        #if something went wrong here, they're not logged in
        print(bcolors.BADRED + 'get_username error' + bcolors.ENDC)
        log_error(e)
        driver.close()
        exit()

#------------------------------------------------------------------------------
#password function
#takes no arguments and returns a string with password in it
def get_password():
    try:
        pword = ''
        #clear pword
        while not pword:
            #loop until a non-empty pword is entered
            pword = getpass.getpass('enter password: ')
        return pword

    except Exception as e:
        #if something went wrong here, they're not logged in
        print(bcolors.BADRED + 'get_password error' + bcolors.ENDC)
        log_error(e)
        driver.close()
        exit()

#------------------------------------------------------------------------------
#deviation page function
#takes nothing and returns a string with the url in it
def get_dev_url():
    try:
        dpage=''
        #clear dpage
        while not dpage:
            #loop until a non-empty deviation url is entered
            dpage = input('paste the deviation\'s URL: ')
        return dpage

    except Exception as e:
        #if something went wrong here, they're not logged in
        print(bcolors.BADRED + 'get_dev_url error' + bcolors.ENDC)
        log_error(e)
        driver.close()
        exit()

#------------------------------------------------------------------------------
#login function
#takes no arguments, modifies driver, and returns nothing
def login():
    try:
        while('deviantart.com/browse/all/' not in driver.current_url):
            #repeat until they log in successfully
            #(it goes to that url when they log in)
            #TODO: more elegant way to check for login
            login_not_me()
            #clear away improper input
            login_send_keys(str(get_username()), str(get_password()))
            #get and send the login keys, until login is successful

    except Exception as e:
        print(bcolors.BADRED + 'login error' + bcolors.ENDC)
        log_error(e)
        driver.close()
        exit()

#------------------------------------------------------------------------------
#login sub_function, used to clear away pre-existing usernames
#takes no arguments, modifies driver, and returns nothing
def login_not_me():
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

#------------------------------------------------------------------------------
#login sub-function, to submit data to the login form
#takes 2 strings, uname and pword, and submits them to the login page.
#returns nothing.
def login_send_keys(uname, pword):
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

    except Exception as e:
        print(bcolors.BADRED + 'login_send_keys error' + bcolors.ENDC)
        log_error(e)
        driver.close()
        exit()

#==============================================================================
#BEYOND THIS POINT, THE WEBDRIVER IS LOGGED IN.
#ERROR HANDLERS MUST LOGOUT TO EXIT THE PROGRAM.
#==============================================================================

#------------------------------------------------------------------------------
#navigation function
#takes a string with the page address, moves webdriver to the deviation page,
#and returns nothing
def get_deviation_page(dpage):
    try:
        driver.get(str(dpage))
        #this tends to delay until the page is fully loaded

    except Exception as e:
        print(bcolors.BADRED + 'get_deviation_page error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#setup function
#takes no arguments, modifies driver, and returns nothing
def open_submission_box():
    try:
        #see if we can find the submit button
        add_button = driver.find_element_by_id \
        ('groups_links')
        #go to the element that holds the button
        add_button = add_button.find_element_by_class_name \
        ('submit_to_groups_link')
        #go to the actual button
        add_button.click()
        #click it to open the box

        #verify the box opened
        element_present = EC.presence_of_element_located \
        ((By.ID, 'manual_input'))
        WebDriverWait(driver, delay).until(element_present)
        #give the popup a delay of up to four seconds to load

    except TimeooutException as e:
        print(bcolors.BADRED, end='')
        print('open_submission_box error: ', \
        'the submission popup took too long to load, or could not be found.', \
        end='')
        print(bcolors.ENDC)
        log_error(e)
        logout()
    except Exception as e:
        print(bcolors.BADRED + 'open_submission_box error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#setup function
#takes no arguments, modifies nothing, returns the modal box
def get_modal_box():
    try:
        return driver.find_element_by_id('modalspace')
        #find the popup box

    except Exception as e:
        print(bcolors.BADRED + 'get_modal_box error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#setup function
#takes no arguments, modifies webdriver, returns nothing
def open_manual_submission():
    try:
        manual_button = modal_box.find_element_by_id \
        ('manual_input')
        #find the manual input button
        manual_button.click()
        #click it

        element_present = EC.presence_of_element_located \
        ((By.ID, 'groupname-search'))
        WebDriverWait(driver, delay).until(element_present)
        #give the entry box a delay of up to four seconds to load

    except Exception as e:
        print(bcolors.BADRED + 'open_submission_box error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#setup function
#takes no arguments, returns an element to the text entry field
def get_entry_field():
    try:
        return modal_box.find_element_by_id('groupname-search')

    except TimeoutException as e:
        print(bcolors.BADRED, end='')
        print('get_entry_field error: ', \
        'the text entry box took too long to load or could not be found.', \
        end='')
        print(bcolors.ENDC)
        log_error(e)
        logout()
    except Exception as e:
        print(bcolors.BADRED + 'get_entry_field error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#setup function
#takes no arguments, returns an element to the text entry field
def get_check_button():
    try:
        return modal_box.find_element_by_id('groupname-check')

    except TimeoutException as e:
        print(bcolors.BADRED, end='')
        print('get_check_button error: ', \
        'the check button took too long to load or could not be found.', \
        end='')
        print(bcolors.ENDC)
        log_error(e)
        logout()
    except Exception as e:
        print(bcolors.BADRED + 'get_check_button error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#automated submission function
#takes a group name, modifies driver by using entry_field and check_button,
#and returns nothing
def send_group_name(name):
    try:
        entry_field.clear()
        #clear any leftover input away
        entry_field.send_keys(name)
        #send the group name
        check_button.click()
        #submit it

        element_present = EC.visibility_of_element_located \
        ((By.CLASS_NAME, 'selected_group_info'))
        WebDriverWait(driver, delay).until(element_present)

    except TimeoutException as e:
        print(handle_group_error())
        pass
    except Exception as e:
        print(bcolors.BADRED + 'send_group_name error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#submission sub-function
#takes nothing, modifies nothing, returns a string containing an error
#message
#gets an error message when a group cannot be submitted to - this covers groups
#that don't exist, can't be submitted to, or already include this deviation
def handle_group_error():
    try:
        error_status = modal_box.find_element_by_class_name('error_message')
        #get the error message box.
        if(error_status.get_attribute('style') == 'display: block;'):
            #the error message is showing. return the text of the message.
            return(str(error_status.find_element_by_tag_name('span').text))
        else:
            #the error message is not showing. return an empty string.
            return ''

    except Exception as e:
        print(bcolors.BADRED + 'handle_group_error error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#logout function
#takes no arguments, modifies the driver, and closes the program
def logout():
    try:
        driver.get('https://www.deviantart.com/settings/sessions')
        logout_button = driver.find_element_by_class_name \
        ('logout-current')
        logout_button.click()
        print(bcolors.GOODGREEN + 'logged out.')

        print('exiting.' + bcolors.ENDC)
        #all clear
        driver.close()
        exit()

    except Exception as e:
        #something went wrong
        print(bcolors.BADRED + 'logout error' + bcolors.ENDC)
        log_error(e)
        driver.close()
        exit()

#==============================================================================
#main function

uname = ''
pword = ''
dpage = ''

do_later = {}
csv_file_name = ''
kword = []

setup()
csv_file_name = get_csv_file()

global driver
driver = open_webdriver()
#declared explicitly as global so any function can close it

login()

dpage = get_dev_url()
get_deviation_page(dpage)
open_submission_box()

global modal_box
modal_box = get_modal_box()
#declared explicitly as global so any function can use it

open_manual_submission()

global entry_field
entry_field = get_entry_field()
global check_button
check_button = get_check_button()
#declared explicitly as global so any function can use these

send_group_name('proving----grounds')
#group that exists
send_group_name('DSGLHLSFHGJDL')
#group that doesn't
send_group_name('proving----grounds')
#group that exists

logout()
