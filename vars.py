
delay = 2
#if something takes longer than 2 seconds, something is up
fieldnames = ['group_name', 'folder_name', 'folder_value']
#these will be used by CSV files

errorlog = './.sys/.errorlog.txt'
errorrec = './.sys/.errorarchive.txt'
savefile = './.sys/.save.txt'
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

global drivr
global modal_box
global entry_field
global check_button
global klist
