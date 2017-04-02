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
from selenium.common.exceptions import WebDriverException
#for if the user closes the browser window
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
        with open('./.sys/.errorlog.txt', 'a') as elog:
            #write error to file
            errordate = str(datetime.datetime.now()) + '\n\n'
            elog.write(errordate)
            elog.write(traceback.format_exc())

        with open('./.sys/.errorarchive.txt', 'a') as earc:
            #write the error to archive
            errordate = str(datetime.datetime.now()) + '\n\n'
            earc.write(errordate)
            earc.write(traceback.format_exc())

            #write a dashed line to make the file easier to read
            dash = '\n'
            for i in range(0,80):
                #make it 80 dashes wide
                dash = dash + '='
            dash = dash + '\n\n'
            #write the dash
            earc.write(dash)

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
        #ensure the .sys folder is created
        if not (os.path.exists('.sys')):
            #sys folder does not exist
            os.makedirs('.sys')

    except Exception as e:
        #i don't anticipate an error ever occuring here
        print(bcolors.BADRED, end='')
        print('setup error: error while checking for .sys folder.', end='')
        print(type(e), '\t\"', e, '\"', end='')
        print(bcolors.ENDC)
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up error log file
        errorlog = './.sys/.errorlog.txt'
        #store name for easier use
        if os.path.isfile(errorlog):
            #if there's an error log, delete it
            os.remove(errorlog)
        with open(errorlog, 'a'):
            #create a blank file for the errorlog
            pass

    except Exception as e:
        #if an error occurs here, it's probably something to do with the
        #error log. this is one of two except functions that won't call
        #log_error, since it would try to reference a bad file.
        print(bcolors.BADRED, end='')
        print('setup error: error while setting up errorlog file.', end='')
        print(type(e), '\t\"', e, '\"', end='')
        print(bcolors.ENDC)
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up permanent error archive file
        errorrec = './.sys/.errorarchive.txt'
        #store the name for easier use
        if not os.path.isfile(errorrec):
            #if there is not an error archive, make one
            with open(errorrec, 'a'):
                pass

    except Exceoption as e:
        #if an error occurs here, it's probably something to do with the
        #error archive. this is one of two except functions that won't call
        #log_error, since it would try to reference a bad file.
        print(bcolors.BADRED, end='')
        print('setup error: error while setting up errorarchive file.', end='')
        print(type(e), '\t\"', e, '\"', end='')
        print(bcolors.ENDC)
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up the replacement file
        replacefile = './.sys/.replace.csv'
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
        #set up the "ask about this later" file
        askfile = './.sys/.ask.csv'
        #store the name for easier use
        if os.path.isfile(askfile):
            #if a file already exists
            pass
        else:
            #we need to create a file
            with open(askfile, 'a') as newfile:
                #create a file for the ask csv
                writer = csv.DictWriter(newfile, fieldnames=fieldnames)
                #writer
                writer.writeheader()
                #write the header

    except Exception as e:
        print(bcolors.BADRED + \
        'setup error: error while setting up ask later file.' +
        bcolors.ENDC)
        log_error(e)
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up the "submit errors" file
        serrorfile = './.sys/.submiterror.csv'
        #store the name for easier use
        if os.path.isfile(serrorfile):
            #if a file already exists
            pass
        else:
            #we need to create a file
            with open(serrorfile, 'a') as newfile:
                #create a file for the ask csv
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
        print(bcolors.BADRED + 'get_csv_file error' + bcolors.ENDC)
        log_error(e)
        exit()

#------------------------------------------------------------------------------
#csv file function
#takes a csv file name, returns nothing
#(will exit program if corruption is detected)
def check_csv_corruption(file):
    try:
        i = 0
        #group number
        corrupt = False

        with open(csv_file_name) as csvfile:
            #open the file to be checked
            reader = csv.DictReader(csvfile)
            #get a reader
            for row in reader:
                #check each row
                if(check_row_corruption(row)):
                    #corrupted
                    print(bcolors.SRSYELLOW, end='')
                    print('warning: corruption detected in group', i, "\n >", \
                    check_row_corruption(row), end='')
                    print(bcolors.ENDC)
                    corrupt = True
                i = i+1

        if(corrupt):
            print(bcolors.WARNYELLOW, end='')
            print('\nplease fix corrupted row(s) before continuing\n(exiting)', \
            end='')
            print(bcolors.ENDC)
            exit()
        else:
            return

    except Exception as e:
        print(bcolors.BADRED + 'get_csv_file error' + bcolors.ENDC)
        log_error(e)
        exit()

#------------------------------------------------------------------------------
#csv file sub-function
#takes a row, changes nothing
#returns empty string if row is not corrupt, error message if it is
def check_row_corruption(row):
    try:
        #check to see if any fields are empty
        #empty folder_name will not actually crash the program, but it's still
        #checked for good practice
        if not(row['group_name']):
            return 'corruption detected: group_name does not exist'
        elif not(row['folder_name']):
            return 'corruption detected: folder_name does not exist'
        elif not(row['folder_value']):
            return 'corruption detected: folder_value does not exist'

        #make sure folder value is a number
        int(row['folder_value'])

        #all tests passed
        return ''

    except ValueError:
        #folder value was not a number
        return 'corruption detected: folder_value is not a number'
    except Exception as e:
        print(bcolors.BADRED + 'check_row_corruption error' + bcolors.ENDC)
        log_error(e)
        exit()

#------------------------------------------------------------------------------
def write_a_row(row, filename):
    try:
        #add the row to the file
        with open(filename, 'a') as csvfile:
            #open file for writing
            writer = csv.writer(csvfile, delimiter=',')
            #get a writer
            writer.writerow(row)
        return
    except Exception as e:
        print(bcolors.BADRED + 'write_a_row error' + bcolors.ENDC)
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

#------------------------------------------------------------------------------
#webdriver function
#takes no arguments, closes driver, and returns an int detailing its status.
#if at any time the webdriver shuts down unexpectedly, this will handle any
#errors associated with it.
def close_webdriver():
    try:
        driver.close()
        return 0
        #return 0 on successful close

    except WebDriverException:
        #the driver was already dead.
        return -1
    except Exception as e:
        #something went wrong, abort the program.
        print(bcolors.BADRED + 'close_webdriver error' + bcolors.ENDC)
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
        close_webdriver()
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
        close_webdriver()
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
        close_webdriver()
        exit()

#------------------------------------------------------------------------------
#login function
#takes no arguments, modifies driver, and returns nothing
def login():
    try:
        while('deviantart.com/browse/all/' not in driver.current_url):
            #repeat until they log in successfully
            #(it goes to that url when they log in)
            login_not_me()
            #clear away improper input
            login_send_keys(str(get_username()), str(get_password()))
            #get and send the login keys, until login is successful

    except Exception as e:
        print(bcolors.BADRED + 'login error' + bcolors.ENDC)
        log_error(e)
        close_webdriver()
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
        close_webdriver()
        exit()

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
        close_webdriver()
        exit()

    except WebDriverException as e:
        #the driver was probably closed already.
        print(bcolors.BADRED + 'logout error' + bcolors.ENDC)
        log_error(e)
        print(bcolors.SRSYELLOW + \
        '\n++++ WARNING: SESSION WAS NOT DEACTIVATED ++++')
        print('go to https://www.deviantart.com/settings/sessions to '\
        'close the session' + bcolors.ENDC)
        close_webdriver()
        exit()
    except Exception as e:
        #something went wrong
        print(bcolors.BADRED + 'logout error' + bcolors.ENDC)
        log_error(e)
        close_webdriver()
        exit()

#==============================================================================
#BEYOND THIS POINT, THE WEBDRIVER IS LOGGED IN.
#ERROR HANDLERS MUST LOGOUT TO EXIT THE PROGRAM.
#==============================================================================

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
            #the error message is not showing. return a generic error.
            error_m = '(handle_group_error was called, but no error message '
            error_m = error_m + 'was showing.)'
            return(error_m)

    except Exception as e:
        print(bcolors.BADRED + 'handle_group_error error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#submission sub-function
#takes nothing, modifies nothing, returns a string containing a message
#gets a success message when a group is successfully submitted to
#returns an empry string otherwise
def get_success_message():
    try:
        success_status = modal_box \
        .find_element_by_class_name('success_message')
        #get the success message box.
        if(success_status.get_attribute('style') == 'display: block;'):
            #the success message is showing. return the text of the message.
            return(str(success_status.find_element_by_tag_name('span').text))
        else:
            #the success message is not showing.
            return ''

    except Exception as e:
        print(bcolors.BADRED + 'get_success_message error' + bcolors.ENDC)
        log_error(e)
        logout()

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
#submission function
#takes a group name, modifies driver by using entry_field and check_button,
#returns nothing on success, error message on failure
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

        #the group info appeared; we can continue
        return ''

    except TimeoutException as e:
        #the group info never appeared - an error probably occurred.
        return(handle_group_error())

    except Exception as e:
        print(bcolors.BADRED + 'send_group_name error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#submission function
#takes no arguments, returns a webelement that can be used to iterate through
#folders available for this gallery
def get_folder_options():
    try:
        folder_element = modal_box.find_element_by_id('gallery_selection')
        #find the selection box
        f_options = folder_element.find_elements_by_tag_name('option')
        #get the folder options, in list form
        return(f_options)
        #return the list of options

    except Exception as e:
        print(bcolors.BADRED + 'get_folder_element error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
#sutomated submission function
#takes a row, submits it with driver, returns nothing
#ignores rows that should be ignored, adds rows to a file if they should be
#asked about later, and submits others.
def process_row(row):
    try:
        g_name = row['group_name']
        f_name = row['folder_name']
        f_val = int(row['folder_value'])
        #save these for ease of use

        if(f_val == -1):
            #not used
            return
        elif(f_val == -2):
            #add to .ask.csv
            write_a_row('./.sys/.ask.csv', row)
            submitasks = submitasks + 1
        else:
            submit_to_folder(row)

    except Exception as e:
        print(bcolors.BADRED + 'process_row error' + bcolors.ENDC)
        log_error(e)
        logout()

#------------------------------------------------------------------------------
def submit_to_folder(row):
    try:
        send_error = send_group_name(row['group_name'])
        #send the group name. if it got an error, handle it.

        if not error:
            #get the folder, click it, and submit
            folderoptions = get_folder_options()
            #get the folders

            for option in folderoptions:
                #iterate through all folders, trying to find the right one
                if(int(option.get_attribute(value)) == \
                int(row['folder_value'])):
                    #a matching value was found
                    option.click()

                    #find the submit button and click it
                    modal_box.find_element_by_class_name('submit').click()

                    #wait for a message to show up
                    #this happens when the option box goes away
                    element_present = EC.invisibility_of_element_located \
                    ((By.CLASS_NAME, 'option_2_box'))
                    WebDriverWait(driver, delay).until(element_present)

                    #get the message
                    message = ''
                    message = get_success_message()

                    if not message:
                        #message was empty, it returned an error
                        print(bcolors.WARNYELLOW + message + bcolors.ENDC)
                        submiterrors = submiterrors + 1

                        #add to error file to process later
                        write_a_row('./.sys/.submiterror.csv', row)

                        return
                    else:
                        #success!
                        print(bcolors.GOODGREEN + message + bcolros.ENDC)
                        submitsuccesses = submitsuccesses + 1

                        return
            #if we reached this point, we went through all the folders but
            #couldn't find the one we were looking for
            #print an error and add it to the list
            message = '(could not find specified folder.)'
            print(bcolors.WARNYELLOW + message + bcolors.ENDC)
            submiterrors = submiterrors + 1

        else:
            #there was an error trying to get the group.
            #print error and do nothing
            print(bcolors.WARNYELLOW + send_error + bcolors.ENDC)
            submitfailures = submitfailures + 1

    except Exception as e:
        print(bcolors.BADRED + 'submit_to_folder error' + bcolors.ENDC)
        log_error(e)
        logout()

#==============================================================================
#main function
if __name__ == "__main__":

    global submitfailures
    submitfailures = 0

    global submiterrors
    submiterrors = 0

    global submitasks
    submitasks = 0

    global submitsuccesses
    submitsuccesses = 0

    setup()
    #run setup functions

    csv_file_name = ''
    csv_file_name = get_csv_file()

    check_csv_corruption(csv_file_name)

    global driver
    driver = open_webdriver()
    #declared explicitly as global so any function can close it

    login()

    get_deviation_page(get_dev_url())
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

    with open(csv_file_name) as csvfile:
        #open the file
        reader = csv.DictReader(csvfile)
        #get a reader
        for row in reader:
            #process all rows
            process_row(row)

    #at this point, automated submissions are complete

    logout()
