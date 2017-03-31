olp_submit program suite (c) Nicholas Reed 2017
Software licensed under Creative Commons 4.0 Share-Alike license
tl;dr do whatever you want with it but don't add extra copyright junk

===============================================================================

SHORT VERSION

this is a set of programs designed to make submitting art to groups on 
deviantART faster. the programs use the Selenium automated testing libraries 
to control a browser window, automating the submission process.



===============================================================================

INSTALLATION GUIDE

(under construction)

===============================================================================

GENERAL USAGE NOTES
- use olp_group_read.py to make a list of groups, olp_list_make to create
  specialized lists for different art types, and olp_submit to submit things
  to dA.
- please don't try to break the program. you probably won't succeed, since
  i preempted a few of the most obvious bugs, but you'll break it eventually if
  you try hard enough.
- once you start using olp_submit.py, the main submission program, don't stop
  until execution is completed - it can't save your progress yet.

===============================================================================

INSTRUCTIONS FOR olp_group_read.py

olp_group_read will go to your groups page and compile all groups into a .csv
file.

- enter your username. that's it.

===============================================================================

INSTRUCTIONS FOR olp_list_make

olp_list_make allows you to create custom lists to submit art of specific types
to specific groups, into specific folders.

- enter your username.
- enter your password. (this data is deleted when you close the program.)
- enter a name for the file. if the file already exists, you may:
  - append to it, or add to the existing file.
  - overwrite it. you will LOSE ALL DATA. proceed with caution!
  - pick a different file name.
- enter keywords. any folder whose name includes a keyword will be highlighted
  for ease of entry.
- decide whether to include a group or ignore it.
- pick the folder you want.

SPECIAL NOTES:
at any text entry field, you can...
- enter "exit" to exit the program.
- enter "a" to include the group, but ask which folder to use each time it
  comes up.
at the folder selection field, you can...
- enter "k" to add new keywords to the list.

===============================================================================

INSTRUCTIONS FOR olp_submit_2

olp_submit_2 will largely automate the process of submitting a deviation to dA
groups.

- enter your username.
- enter your password. (this data is deleted when you close the program.)
- enter the URL of the deviation you want to submit to groups.
- enter the name of the list you want to use.
- enter any keywords you want to use, for the same reason as in olp_list_make.
- wait for automated submission to finish.
- manually submit other deviations.

SPECIAL NOTES:
- if you choose to update a preferred folder, your preferences are saved in
  a CSV file called ".replace.csv" - the actual update process has not been
  tested yet as of 03-22-2017. if it does not work, try manually updating the
  csv file with your preferred editor, such as MS Excel or a text editor.
