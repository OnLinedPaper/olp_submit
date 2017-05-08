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
from selenium.common.exceptions import StaleElementReferenceException
#for if the user submits to a group that can be used
from selenium.common.exceptions import NoSuchWindowException
#for if the user closes the window
from selenium.common.exceptions import NoSuchElementException
#for if an element gets lost somewhere
from selenium.webdriver.common.by import By
#also used when waiting for stuff to load
#bunch of selenium things
import signal
#to catch CTRL+C
import shelve
#for persistent data storage

import sys
#lots of good stuff in here
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
import time
#for writing my own delays

import vars as v

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
#print function
#takes no arguments, returns nothing
#prints a warning to users, letting them know their session may still be active
def print_active_session_warning():

    try:
        print(bcolors.SRSYELLOW, end='')
        print('\n\n\n    !! WARNING: LOGIN SESSION MAY STILL BE ACTIVE. !!')
        print('( check at https://www.deviantart.com/settings/sessions )')
        print(bcolors.ENDC, end='')

    except:
        pass

#------------------------------------------------------------------------------
#save file function
#takes no arguments, tries to close the save file, returns nothing
def close_save_file():

    try:
        v.s.close()
        #save current data

    except TypeError:
        #the save file wasn't open
        pass

#------------------------------------------------------------------------------
#signal handling function, designed to catch Ctrl-C and exit gracefully
def signal_handler(signal, frame):

    try:
        close_save_file()

        print_active_session_warning()

        print(bcolors.GOODGREEN + '\nexiting.' + bcolors.ENDC)

    except:
        pass

    exit()

#------------------------------------------------------------------------------
#custom excepthook to catch the exception thrown if the user accidentally
#closes the browser window, loses internet connection, or any other error
def except_hook(exctype, value, traceback):

    try:
        v.s.close()
        #save the state
    except TypeError as e:
        #the save file wasn't open
        pass

    try:
        if exctype == ConnectionRefusedError:
            #connection was lost
            print(bcolors.BADRED + "failure: connection lost." + bcolors.ENDC)
        elif exctype == NoSuchWindowException:
            #window closed
            print(bcolors.BADRED + "failure: window lost." + bcolors.ENDC)
        elif exctype == NoSuchElementException:
            #element was not found
            print(bcolors.BADRED + "failure: missing element." + bcolors.ENDC)
        else:
            #it was some other error, let system handle it
            sys.__excepthook__(exctype, value, traceback)
    except:
        #something went wrong, just let the system handle it
        sys.__excepthook__(exctype, value, traceback)

#------------------------------------------------------------------------------
#error logging function
#takes a string and prints a traceback to an error file, as well as the string
#to stdout
def log_error(e):
    try:
        with open(v.errorlog, 'a') as elog:
            #write error to file
            errordate = str(datetime.datetime.now()) + '\n\n'
            elog.write(errordate)
            elog.write(traceback.format_exc())

        with open(v.errorrec, 'a') as earc:
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

            print_active_session_warning()

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
#takes a file name, saves it, and returns nothing
def save_curr_file(fname):
    try:
        v.s['curr_file'] = fname

    except Exception as e:
        print(bcolors.BADRED + 'save_curr_file error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#takes a url, saves it, and returns nothing
def save_curr_url(url):
    try:
        v.s['curr_url'] = url

    except Exception as e:
        print(bcolors.BADRED + 'save_curr_url error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#takes a row, saves it, and returns nothing
def save_curr_group(group):
    try:
        v.s['curr_group'] = group

    except Exception as e:
        print(bcolors.BADRED + 'save_curr_group error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#takes a status, saves it, and returns nothing
def set_curr_status(status):
    try:
        v.s['curr_status'] = int(status)

    except Exception as e:
        print(bcolors.BADRED + 'set_curr_status error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#basic function
#takes no arguments, asks user a yes/no question, returns y on yes and
#empty string on no
def get_yes_no():
    try:
        ans = ''
        #set as blank and then enter a loop to ask user
        while not any(s in ans[:1] for s in ['y', 'n']):
            ans = input('(y\\n): ')

        if('y' in ans[:1]):
            #answer was yes
            return('y')
        else:
            #answer was no
            return ''

    except Exception as e:
        print(bcolors.BADRED + 'get_yes_no error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#==============================================================================

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
            close_save_file()
            exit()

    except Exception as e:
        #i don't anticipate an error ever occuring here
        print(bcolors.BADRED, end='')
        print('setup error: error while checking for data folder.', end='')
        print(type(e), '\t\"', e, '\"', end='')
        print(bcolors.ENDC)
        close_save_file()
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
        close_save_file()
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #ensure the .sys/.savedata folder is created
        if not (os.path.exists('.sys/.savedata')):
            #savedata folder does not exist
            os.makedirs('.sys/.savedata')

    except Exception as e:
        #i don't anticipate an error ever occuring here
        print(bcolors.BADRED, end='')
        print('setup error: error while checking for savedata folder.', end='')
        print(type(e), '\t\"', e, '\"', end='')
        print(bcolors.ENDC)
        close_save_file()
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up error log file
        if os.path.isfile(v.errorlog):
            #if there's an error log, delete it
            os.remove(v.errorlog)
        with open(v.errorlog, 'a'):
            pass

    except Exception as e:
        #if an error occurs here, it's probably something to do with the
        #error log. this is one of two except functions that won't call
        #log_error, since it would try to reference a bad file.
        print(bcolors.BADRED, end='')
        print('setup error: error while setting up errorlog file.', end='')
        print(type(e), '\t\"', e, '\"', end='')
        print(bcolors.ENDC)
        close_save_file()
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up permanent error archive file
        if not os.path.isfile(v.errorrec):
            #if there is not an error archive, make one
            with open(v.errorrec, 'a'):
                pass

    except Exception as e:
        #if an error occurs here, it's probably something to do with the
        #error archive. this is one of two except functions that won't call
        #log_error, since it would try to reference a bad file.
        print(bcolors.BADRED, end='')
        print('setup error: error while setting up errorarchive file.', end='')
        print(type(e), '\t\"', e, '\"', end='')
        print(bcolors.ENDC)
        close_save_file()
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up save file

        #assign the dict to global variable v.s
        v.s = shelve.open(v.savefile)

        try:
            stat = v.s['curr_status']
            stat = int(stat)

            if(stat != int(-1)):
                print(bcolors.GOODGREEN, end='')
                #there is an active session.
                print('\na save file has been detected.')
                print('current csv file: ' + v.s['curr_file'])
                print('current status: ', end='')

                #status switch
                if(stat == 0):
                    print('in setup')
                elif(stat == 1):
                    print('in automated submissions')
                elif(stat == 2):
                    print('in manual submissions')

                while(1):
                    #check to see if they want to use the sace data
                    print(bcolors.GOODGREEN, end='')
                    print('\nuse current file? ', end='')
                    if not get_yes_no():
                        #they don't want to use the save file
                        print(bcolors.SRSYELLOW, end='')
                        print('\ndelete save file? ', end='')
                        if get_yes_no():
                            #they want to delete the file
                            set_curr_status(-1)

                            print(bcolors.GOODGREEN, end='')
                            print('save file deleted.\n')

                            #end the loop
                            break
                    else:
                        #preserve the save data and end the loop
                        print(bcolors.GOODGREEN, end='')
                        print('using current file.\n')
                        break

                print(bcolors.ENDC, end='')

        except KeyError as e:
            #a save file did not exist; opening it has created it.
            set_curr_status(-1)

    except Exception as e:
        print(bcolors.BADRED, end='')
        print('setup error: error while setting up save file.' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up the replacement file
        if not os.path.isfile(v.replacefile):
            #if there's not a preexisting replace file
            with open(v.replacefile, 'a') as newfile:
                #create a file for the replace csv
                writer = csv.DictWriter(newfile, fieldnames=v.fieldnames)
                #writer
                writer.writeheader()
                #write the header

    except Exception as e:
        print(bcolors.BADRED + \
        'setup error: error while setting up replace file.' + \
        bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up the "ask about this later" file
        if not os.path.isfile(v.askfile):
            #if a file does not already exist
            #we need to create a file
            with open(v.askfile, 'a') as newfile:
                #create a file for the ask csv
                writer = csv.DictWriter(newfile, fieldnames=v.fieldnames)
                #writer
                writer.writeheader()
                #write the header

    except Exception as e:
        print(bcolors.BADRED + \
        'setup error: error while setting up ask later file.' + \
        bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up the "submit errors" file
        if not os.path.isfile(v.serrorfile):
            #if a file does not exist
            #we need to create a file
            with open(v.serrorfile, 'a') as newfile:
                #create a file for the ask csv
                writer = csv.DictWriter(newfile, fieldnames=v.fieldnames)
                #writer
                writer.writeheader()
                #write the header

    except Exception as e:
        print(bcolors.BADRED + \
        'setup error: error while setting up error handling file.' + \
        bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

    #-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    try:
        #set up the "submit limit" file
        if not os.path.isfile(v.slimitfile):
            #if a file does not yet exist
            #we need to create a file
            with open(v.slimitfile, 'a') as newfile:
                #create a file for the ask csv
                writer = csv.DictWriter(newfile, fieldnames=v.fieldnames)
                #writer
                writer.writeheader()
                #write the header

    except Exception as e:
        print(bcolors.BADRED + \
        'setup error: error while setting up limit handling file.' + \
        bcolors.ENDC)
        log_error(e)
        close_save_file()
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
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#csv file function
#takes a csv file name, returns nothing
#(will exit program if corruption is detected)
def check_csv_corruption(csv_file_name):
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
            close_save_file()
            exit()
        else:
            return

    except Exception as e:
        print(bcolors.BADRED + 'get_csv_file error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
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
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#csv file function
#accepts a csv file name and a row, opens it in append mode, and writes the
#specified row to that file in append mode.
#returns nothing.
def write_a_row(filename, row):
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
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#csv file function
#takes a file name as an argument, counts the number of rows that will be
#submitted (anything that's not "-1") and returns this value as an int
def get_row_count(filename):
    try:
        group_count = 0;

        #open the filename
        with open(filename) as csvfile:
            #open file to read
            reader = csv.DictReader(csvfile)

            for row in reader:
                    group_count += 1

        #send the count back
        return group_count

    except Exception as e:
        print(bcolors.BADRED + 'get_submittable_rows error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
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
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#webdriver function
#takes no arguments, closes driver, and returns an int detailing its status.
#if at any time the webdriver shuts down unexpectedly, this will handle any
#errors associated with it.
def close_webdriver():
    try:
        v.drivr.close()
        return 0
        #return 0 on successful close

    except WebDriverException:
        #the driver was already dead.
        return -1
    except Exception as e:
        #something went wrong, abort the program.
        print(bcolors.BADRED + 'close_webdriver error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
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
        close_save_file()
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
        close_save_file()
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

        save_curr_url(dpage)
        #save the current URL
        return dpage

    except Exception as e:
        #if something went wrong here, they're not logged in
        print(bcolors.BADRED + 'get_dev_url error' + bcolors.ENDC)
        log_error(e)
        close_webdriver()
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#login function
#takes no arguments, modifies driver, and returns nothing
def login():
    try:
        v.drivr.get('https://www.deviantart.com/users/login')

        while('/users/' in v.drivr.current_url):
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
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#login sub_function, used to clear away pre-existing usernames
#takes no arguments, modifies driver, and returns nothing
def login_not_me():
    try:
        #if they entered an existing uname, go back to the
        #original entry page
        not_me = v.drivr.find_element_by_class_name \
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
        v.drivr.get('https://www.deviantart.com/users/login')
        #go to the login page
        login_elem = v.drivr.find_element_by_id \
        ('login_username')
        #go to the username field
        login_elem.clear()
        #clear any existing text out of the username field
        login_elem.send_keys(uname)
        #put in username

        login_elem = v.drivr.find_element_by_id \
        ('login_password')
        #go to password field
        login_elem.clear()
        #clear out any existing text
        login_elem.send_keys(pword)
        #put in password

        login_elem = v.drivr.find_element_by_id \
        ('remember_me')
        #go to "remember me" checkbox
        login_elem.click()
        #uncheck it

        login_elem = v.drivr.find_element_by_class_name \
        ('smbutton')
        #go to login button
        login_elem.click()
        #click it to log in

    except Exception as e:
        print(bcolors.BADRED + 'login_send_keys error' + bcolors.ENDC)
        log_error(e)
        close_webdriver()
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#logout function
#takes no arguments, modifies the driver, and closes the program
def logout():
    try:
        v.drivr.get('https://www.deviantart.com/settings/sessions')
        logout_button = v.drivr.find_element_by_class_name \
        ('logout-current')
        logout_button.click()
        print(bcolors.GOODGREEN + 'logged out.')

        print('exiting.' + bcolors.ENDC)
        #all clear
        close_webdriver()
        close_save_file()
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
        close_save_file()
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
        error_status = v.modal_box.find_element_by_class_name('error_message')
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
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#submission sub-function
#takes nothing, modifies nothing, returns a string containing a message
#gets a success message when a group is successfully submitted to
#returns an empry string otherwise
def get_success_message():
    try:
        success_status = v.modal_box \
        .find_element_by_class_name('success_message')
        #get the success message box.
        error_status = v.modal_box \
        .find_element_by_class_name('error_message')
        #get the error message box.

        cust_delay = time.time() + v.delay
        #set a 4 second timer

        while(cust_delay > time.time()):
            #while the custom delay has not expired

            if(success_status.get_attribute('style') != 'display: block;'\
            and error_status.get_attribute('style') != 'display: block;'):
                #neither is visible - refresh both

                success_status = v.modal_box \
                .find_element_by_class_name('success_message')
                #refresh the success message box.
                error_status = v.modal_box \
                .find_element_by_class_name('error_message')
                #refresh the error message box.
            else:
                #one of them showed up
                break

        if(success_status.get_attribute('style') == 'display: block;'):
            #the success message is showing. return the text of the message.
            return(str(success_status.find_element_by_tag_name('span').text))
        else:
            #the success message is not showing.
            return ''

    except Exception as e:
        print(bcolors.BADRED + 'get_success_message error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#navigation function
#takes a string with the page address, moves webdriver to the deviation page,
#and returns nothing
def get_deviation_page(dpage):
    try:
        v.drivr.get(str(dpage))
        #this tends to delay until the page is fully loaded

    except Exception as e:
        print(bcolors.BADRED + 'get_deviation_page error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#setup function
#takes no arguments, modifies driver, and returns nothing
def open_submission_box():
    try:
        #see if we can find the submit button
        add_button = v.drivr.find_element_by_id \
        ('groups_links')
        #go to the sub-element that holds the button
        add_button = add_button.find_element_by_class_name \
        ('submit_to_groups_link')
        #go to the element that holds the button
        add_button = add_button.find_element_by_class_name \
        ('jslink')
        #go to the actual button
        add_button.click()
        #click it to open the box

        #verify the box opened
        element_present = EC.presence_of_element_located \
        ((By.ID, 'manual_input'))
        WebDriverWait(v.drivr, v.delay).until(element_present)
        #give the popup a delay of up to four seconds to load

    except TimeoutException as e:
        print(bcolors.BADRED, end='')
        print('open_submission_box error: ', \
        'the submission popup took too long to load, or could not be found.', \
        end='')
        print(bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()
    except Exception as e:
        print(bcolors.BADRED + 'open_submission_box error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#setup function
#takes no arguments, modifies nothing, returns the modal box
def get_modal_box():
    try:
        return v.drivr.find_element_by_id('modalspace')
        #find the popup box

    except Exception as e:
        print(bcolors.BADRED + 'get_v.modal_box error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#setup function
#takes no arguments, modifies webdriver, returns nothing
def open_manual_submission():
    try:
        manual_button = v.modal_box.find_element_by_id \
        ('manual_input')
        #find the manual input button
        manual_button.click()
        #click it

        element_present = EC.presence_of_element_located \
        ((By.ID, 'groupname-search'))
        WebDriverWait(v.drivr, v.delay).until(element_present)
        #give the entry box a delay of up to four seconds to load

    except Exception as e:
        print(bcolors.BADRED + 'open_submission_box error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#setup function
#takes no arguments, returns an element to the text entry field
def get_entry_field():
    try:
        return v.modal_box.find_element_by_id('groupname-search')

    except TimeoutException as e:
        print(bcolors.BADRED, end='')
        print('get_entry_field error: ', \
        'the text entry box took too long to load or could not be found.', \
        end='')
        print(bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()
    except Exception as e:
        print(bcolors.BADRED + 'get_entry_field error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#setup function
#takes no arguments, returns an element to the text entry field
def get_check_button():
    try:
        return v.modal_box.find_element_by_id('groupname-check')

    except TimeoutException as e:
        print(bcolors.BADRED, end='')
        print('get_check_button error: ', \
        'the check button took too long to load or could not be found.', \
        end='')
        print(bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()
    except Exception as e:
        print(bcolors.BADRED + 'get_check_button error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#submission function
#takes a group name, modifies driver by using v.entry_field and v.check_button,
#returns nothing on success, error message on failure
def send_group_name(name):
    try:
        v.entry_field.clear()
        #clear any leftover input away
        v.entry_field.send_keys(name)
        #send the group name
        v.check_button.click()
        #submit it

        element_visible = EC.visibility_of_element_located \
        ((By.CLASS_NAME, 'selected_group_info'))
        WebDriverWait(v.drivr, v.delay).until(element_visible)

        #the group info appeared; we can continue
        return ''

    except TimeoutException:
        #the group info never appeared - an error probably occurred.
        return(handle_group_error())

    except Exception as e:
        print(bcolors.BADRED + 'send_group_name error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#submission function
#takes no arguments, returns a webelement that can be used to iterate through
#folders available for this gallery
def get_folder_options():
    try:
        folder_element = v.modal_box.find_element_by_id('gallery_selection')
        #find the selection box
        f_options = folder_element.find_elements_by_tag_name('option')
        #get the folder options, in list form
        return(f_options)
        #return the list of options

    except Exception as e:
        print(bcolors.BADRED + 'get_folder_options error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#submission function
#takes a list of folders, prints folders out with keywords highlighted, and
#returns the number of folders printed.
def print_folders(folders):
    try:
        folder_num = 0
        print('\nuse which folder?')
        for folder in folders:
            folder_num += 1
            print('folder', end='')

            #spacing to make it look better
            if(folder_num < 10):
                print('   #', end='')
            elif(folder_num < 100):
                print('  #', end='')
            print(str(folder_num) + ': ', end='')

            for word in v.klist:
                if(word.lower() in folder.text.lower()):
                    #keyword match
                    print(bcolors.GOODGREEN, end='')
            #print each folder name
            print(folder.text + bcolors.ENDC)

        #extra options
        print('option # i: (ignore group this time)')
        print('option # s: (stop using this group)')
        print('option # a: (ask in the future)')

        return folder_num
        #so that we can check to see if the folder is in bounds

    except Exception as e:
        print(bcolors.BADRED + 'print_folders error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#sutomated submission function
#takes a row, submits it with driver, returns nothing
#ignores rows that should be ignored, adds rows to a file if they should be
#asked about later, and submits others.
def process_row(row):
    try:
        f_val = int(row['folder_value'])
        #save this for ease of use

        if(f_val == -1):
            #not used
            return
        elif(f_val == -2):
            message = ''
            message = send_group_name(row['group_name'])
            if not message:
                #no error was showing; we can ask the user
                #add to .ask.csv
                write_me = [row['group_name'], \
                row['folder_name'], row['folder_value']]
                write_a_row(v.askfile, write_me)
                print(bcolors.GOODGREEN + \
                'asking after automated submissions complete' + bcolors.ENDC)
                v.submitasks = v.submitasks + 1
            else:
                print('\ngroup:', row['group_name'])
                print(bcolors.WARNYELLOW + message + bcolors.ENDC)
                v.submitfailures = v.submitfailures + 1
        else:
            submit_to_folder(row)

        save_curr_group(row['group_name'])
        #save row for later

    except Exception as e:
        print(bcolors.BADRED + 'process_row error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#automated submission function
#takes a row as argument, submits it to the group, and returns nothing
def submit_to_folder(row):
    try:
        print('\nfor group: \"' + row['group_name'] +'\"')

        send_error = send_group_name(row['group_name'])
        #send the group name. if it got an error, handle it.

        if not send_error:
            #get the folder, click it, and submit
            folderoptions = get_folder_options()
            #get the folders

            for option in folderoptions:
                #iterate through all folders, trying to find the right one
                if(int(option.get_attribute('value')) == \
                int(row['folder_value'])):
                    #a matching folder value was found
                    option.click()

                    #find the submit button and click it
                    v.modal_box.find_element_by_class_name('submit').click()

                    #wait for a message to show up
                    #this happens when the option box goes away
                    element_present = EC.invisibility_of_element_located \
                    ((By.CLASS_NAME, 'option_2_box'))
                    WebDriverWait(v.drivr, v.delay).until(element_present)

                    #get the message
                    message = ''
                    message = get_success_message()

                    if not message:
                        #message was empty, it returned an error
                        message = handle_group_error()
                        print(bcolors.WARNYELLOW + message + bcolors.ENDC)

                        write_me = [row['group_name'], \
                        row['folder_name'], row['folder_value']]

                        if 'size' in message:
                            #folder was over size limit
                            write_a_row(v.serrorfile, write_me)
                            v.submiterrors = v.submiterrors + 1
                        elif 'limit' in message:
                            #user hit submission limit
                            write_a_row(v.slimitfile, write_me)
                            v.submitlimits = v.submitlimits + 1
                        else:
                            #needs to be addressed
                            write_a_row(v.serrorfile, write_me)
                            v.submiterrors = v.submiterrors + 1

                        return
                    else:
                        #success!
                        print(bcolors.GOODGREEN + message + bcolors.ENDC)
                        if('pending' in message):
                            #pending approval
                            v.submitpendings = v.submitpendings + 1
                        else:
                            #approved automatically
                            v.submitsuccesses = v.submitsuccesses + 1

                        return
            #if we reached this point, we went through all the folders but
            #couldn't find the one we were looking for
            #print an error and add it to the list
            message = '(could not find specified folder.)'
            print(bcolors.WARNYELLOW + message + bcolors.ENDC)
            write_a_row(v.serrorfile, row)
            v.submiterrors = v.submiterrors + 1

        else:
            #there was an error trying to get the group.
            #print error and do nothing
            print(bcolors.WARNYELLOW + send_error + bcolors.ENDC)
            v.submitfailures = v.submitfailures + 1

    except TimeoutException:
        #couldn't submit it, just ignore it.
        message = '(submit_to_folder warning: something took too long.)'
        print(bcolors.WARNYELLOW + message + bcolors.ENDC)

        write_me = [row['group_name'], \
        row['folder_name'], row['folder_value']]
        write_a_row(v.serrorfile, write_me)
        #continue with normal operation
        return

    except Exception as e:
        print(bcolors.BADRED + 'submit_to_folder error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#manual submission function
#takes a csv inname and a csv filename as arguments, returns 1 to process, 0 to
#not process but also not delete, -1 if the file was deleted
def ask_about_processing(inname, filename):
    try:
        name = str(inname)
        #in case they name it a number (would break print functions)
        response = ''
        while not any(s in response for s in ['y', 'l']):
            #get them to answer yes or later ('no' means they want to delete)
            message = '\nprocess '
            message = message + name
            message = message + '? yes\\no\\later (y\\n\\l): '
            response = input(message)
            if(response == 'y'):
                return 1
            elif(response == 'l'):
                #continue, but don't delete file
                return 0
            elif(response == 'n'):
                #see if they want to delete file
                message = 'delete '
                message = message + name
                message = message + '? yes\\no (y\\n): '
                response = input(message)
                if(response == 'y'):
                    #delete it. if they respond with anything else, it will just
                    #loop back to the top.
                    os.remove(filename)
                    print(bcolors.SRSYELLOW + 'deleted', name + bcolors.ENDC)
                    return -1

    except Exception as e:
        print(bcolors.BADRED + 'ask_about_processing error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#takes no arguments, modifies v.klist, and returns nothing
#gets a string of user entered keywords and adds them to v.klist
def get_keywords():
    try:
        new_k = input('enter keywords: ')
        #get their keywords
        if new_k:
            #not empty, add keywords
            new_klist = re.sub('[^\w]', ' ', new_k).split()
            v.klist = v.klist + new_klist
            print('keywords: ' + bcolors.GOODGREEN)
            for word in v.klist:
                #echo keywords
                print(word)
            print(bcolors.ENDC)
        else:
            #nothing added
            print('no keywords added.')

    except Exception as e:
        print(bcolors.BADRED + 'get_keywords error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
#manual processing function
#accepts a file name as an argument, and then guides the user through the
#process of manually selecting which folder they would like to submit the
#deviation to for any valid groups
def manually_process(filename):
    try:
        with open(filename) as csvfile:
            #open the file
            reader = csv.DictReader(csvfile)
            #get a reader
            for row in reader:
                error_message = ''
                error_message = send_group_name(row['group_name'])
                #make sure this is a valid group

                if not error_message:
                    choice = -1

                    while(str(choice) == '-1'):
                        #send the group name
                        opt = get_folder_options()
                        #get the options

                        print('\nfor group: ', row['group_name'])
                        folder_num = 0
                        folder_num = print_folders(opt)
                        #print the folder options
                        try:
                            choice = input('folder #')
                            if(str(choice) == 'i'):
                                #ignore it
                                print('ignored.')

                                choice = -1
                                break
                            elif(str(choice) == 's'):
                                #eliminate it.
                                write_a_row(v.replacefile, \
                                [row['group_name'], 'UNUSED', '-1'])
                                print('group removed.')

                                choice = -1
                                break
                            elif(str(choice) == 'a'):
                                #ask each time in the future.
                                write_a_row(v.replacefile, \
                                [row['group_name'], 'ASK', '-2'])
                                print('asking next time.')

                                choice = -1
                                break
                            elif(str(choice) == 'k'):
                                #get keywords
                                get_keywords()

                                choice = -1
                                pass
                            elif(str(choice) == 'x'):
                                #save and exit
                                close_save_file()
                                exit()
                            elif(str(choice) == 'p'):
                                #reprint folder options
                                print('for group:', row['group_name'])
                                folder_num = print_folders(opt)

                                choice = -1
                                pass
                            elif(int(choice) > folder_num or int(choice) <= 0):
                                #bad folder number
                                print('folder out of bounds.')

                                choice = -1
                                pass
                            else:
                                pick = 0
                                #process this row
                                for fld in opt:
                                #find their folder
                                    pick += 1
                                    if(int(pick) == int(choice)):
                                        #it's this folder
                                        fld.click()
                                        #find the submit button and click it
                                        v.modal_box.find_element_by_class_name \
                                        ('submit').click()

                                        #get the message
                                        message = ''
                                        message = get_success_message()

                                        if not message:
                                            #message was empty,
                                            #it returned an error
                                            message = handle_group_error()
                                            print(bcolors.WARNYELLOW + \
                                            message + bcolors.ENDC)

                                            #get folder options again
                                            send_group_name(row['group_name'])
                                            #try again
                                            choice = -1
                                        else:
                                            #success!
                                            print(bcolors.GOODGREEN + \
                                            message + bcolors.ENDC)


                        except ValueError:
                            #print nothing; just get folder num again
                            choice = -1
                else:
                    print(bcolors.BADRED, end='')
                    print(error_message, end='')
                    print(bcolors.ENDC)

                save_curr_group(row['group_name'])
                #save row for later

    except FileNotFoundError:
        #file was already processed or was not found
        print('file not found: \'' + filename +'\'')

        return

    except Exception as e:
        print(bcolors.BADRED + 'manually_process error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#==============================================================================
#main subfunctions

#------------------------------------------------------------------------------
def get_parameters_from_user():
    try:
        csv_file_name = ''
        csv_file_name = get_csv_file()

        print('checking csv file for corruption... ', end='')
        check_csv_corruption(csv_file_name)
        #ask user for csv file name
        print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

        save_curr_file(csv_file_name)
        #start the save data

        print('opening webdriver... ', end='')
        v.drivr = open_webdriver()
        print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

        print('getting login information... ')
        login()
        print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

        print('getting deviation page... ')
        get_deviation_page(get_dev_url())
        #ask user for URL
        #(this function saves url)
        print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

    except Exception as e:
        print(bcolors.BADRED + 'get_parameters_from_user error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#------------------------------------------------------------------------------
def get_parameters_from_save():
    try:
        csv_file_name = ''
        csv_file_name = v.s['curr_file']
        #load CSV file from save

        print('checking csv file for corruption... ', end='')
        check_csv_corruption(csv_file_name)
        print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

        print('opening webdriver... ', end='')
        v.drivr = open_webdriver()
        print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

        print('getting login information... ')
        login()
        print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

        print('getting deviation page... ')
        get_deviation_page(v.s['curr_url'])
        #load URL from save file
        print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

    except Exception as e:
        print(bcolors.BADRED + 'get_parameters_from_save error' + bcolors.ENDC)
        log_error(e)
        close_save_file()
        exit()

#==============================================================================
#main function
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    #to catch ctrl-c
    sys.excepthook = except_hook
    #to catch some errors

    print('running setup tasks...')
    setup()
    #run setup functions
    print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

    #load user's parameters
    if(int(v.s['curr_status']) == int(-1)):
        #no save file exists
        get_parameters_from_user()

        set_curr_status(0)
        #set status to zero to indicate things are happening
    else:
        #a save file exists
        get_parameters_from_save()

    csv_file_name = ''
    csv_file_name = v.s['curr_file']
    #get the current file


    print('opening submission box... ', end='')
    open_submission_box()
    print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

    print('opening modal box... ', end='')
    v.modal_box = get_modal_box()
    print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

    print('opening submission box... ', end='')
    open_manual_submission()
    print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)


    print('getting entry field... ', end='')
    v.entry_field = get_entry_field()
    print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)

    print('getting check button... ', end='')
    v.check_button = get_check_button()
    print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)


    print('getting row count... ', end='')
    grouptotal = get_row_count(csv_file_name)
    #get the total number of rows
    print(bcolors.GOODGREEN + 'done.\n' + bcolors.ENDC)


    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    #automated submissions

    groupnum = 0


    if(int(v.s['curr_status']) == int(0)):
        #nothing was in progress: start manual submissions

        print('\nbeginning automatic submissions.\n')

        set_curr_status(1)
        #working on automatic submissions

        with open(csv_file_name) as csvfile:
            #open the file
            reader = csv.DictReader(csvfile)
            #get a reader

            for row in reader:
                #process all rows
                process_row(row)

                #print where we are
                groupnum += 1
                print('(group', str(groupnum), "of", str(grouptotal) + ")")

    elif(int(v.s['curr_status']) == int(1)):
        #automatic submissions were in progress
        #fast forward to where they were

        print('\ncontinuing automatic submissions.\n')

        with open(csv_file_name) as csvfile:
            #open the file
            reader = csv.DictReader(csvfile)
            #get a reader

            cont = 0;
            #we will use this to fast forward to the current row

            for row in reader:
                if not cont:
                    #we haven't found the row yet
                    try:
                        if(v.s['curr_group'] == row['group_name']):
                            #group names match
                            #(checking on group names because dA guarantees
                            #these will be unique, but other values may not be,
                            #i.e. ASK or UNUSED folders)
                            cont = 1
                            #resume processing
                        else:
                            #skip this one
                            groupnum += 1
                    except EOFError:
                        #will happen if key lookup fails
                        print(bcolors.WARNYELLOW + \
                        'warning: group not found. save file may be corrupt.',\
                        end='')
                        print(bcolors.ENDC)
                        logout()

                else:
                    #process all remaining rows
                    process_row(row)

                    #print where we are
                    groupnum += 1
                    print('(group', str(groupnum), "of", str(grouptotal) + ")")

        #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        #manual submissions
        #at this point, automated submissions are complete

        print(bcolors.GOODGREEN + \
            'automated submissions complete')
        print(str(v.submitsuccesses) + \
            ' successful')
        print(str(v.submitpendings) + \
            ' pending')
        print(str(v.submitasks) + \
            ' asks')
        print(bcolors.WARNYELLOW + str(v.submitlimits) + \
            ' unsuccessful (limit)')
        print(bcolors.SRSYELLOW + str(v.submiterrors) + \
            ' unsuccessful (error)')
        print(bcolors.BADRED + str(v.submitfailures) + \
            ' failed' + bcolors.ENDC)

        set_curr_status(2)

    #other submissions

    v.klist = []

    get_keywords()

    #see if they want to do asks
    if(int(ask_about_processing('asks', v.askfile)) == 1):
        #they want to do asks
        manually_process(v.askfile)
        try:
            os.remove(v.askfile)
        except FileNotFoundError:
            #file wasn't there
            pass

    #see if they want to do limit errors
    if(int(ask_about_processing('limit errors', v.slimitfile)) == 1):
        #they want to do asks
        manually_process(v.slimitfile)
        try:
            os.remove(v.slimitfile)
        except FileNotFoundError:
            #file wasn't there
            pass

    #see if they want to do regular errors
    if(int(ask_about_processing('other errors', v.serrorfile)) == 1):
        #they want to do asks
        manually_process(v.serrorfile)
        try:
            os.remove(v.serrorfile)
        except FileNotFoundError:
            #file wasn't there
            pass


    print('\nall submissions complete.\ncleaning up... ', end='')

    try:
        set_curr_status(-1)
        #nothing else in here matters
    except:
        #don't ever expect an error here
        pass

    print(bcolors.GOODGREEN + 'done.' + bcolors.ENDC)

    logout()
