
delay = 2
#if something takes longer than 2 seconds, something is up
fieldnames = ['group_name', 'folder_name', 'folder_value']
#these will be used by CSV files

errorlog = './.sys/.errorlog.txt'
errorrec = './.sys/.errorarchive.txt'
savefile = './.sys/.savedata/.save'
replacefile = './.sys/.replace.csv'
askfile = './.sys/.ask.csv'
serrorfile = './.sys/.submiterror.csv'
slimitfile = './.sys/.submitlimit.csv'
#store the names for easier use

activefile = ''
activegroup = ''

submitfailures = 0
submitlimits = 0
submiterrors = 0
submitasks = 0
submitsuccesses = 0
submitpendings = 0

global drivr
global modal_box
global entry_field
global check_button
global klist


global s

#save dict structure:
    #curr_status:
        #-1 (nothing)
        #0 (exists but not started)
        #1 (was working on automated submissions)
        #2 (was working on manual submissions)
    #curr_file:
        #the CSV file
    #curr_url:
        #the URL
    #curr_group:
        #the group
