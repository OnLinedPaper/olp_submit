import csv
import os
import submit_v3 as s

if __name__ == "__main__":
    #use submit_v3's functions to get the source file name
    print('(source) | ', end='')
    source_file_name = s.get_csv_file()

    #get new file name
    print('(new file) | ', end='')

    try:
        csv_file_name = ''
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

    except Exception as e:
        print('error getting new filename')
        exit()


    with open(csv_file_name, 'a') as newfile:
        #write the new file's header
        fieldnames = ['group_name', 'folder_name', 'folder_value']

        writer = csv.DictWriter(newfile, fieldnames=fieldnames)
        writer.writeheader()

#-   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
#make the seed

    with open(source_file_name) as sourcefile:
        reader = csv.DictReader(sourcefile)
        with open(csv_file_name, 'a') as csvfile:
            #open file for writing
            writer = csv.writer(csvfile, delimiter=',')
            #get a writer

            for row in reader:
                if(int(row['folder_value']) != -2):
                    #this is not an ask
                    #it's either ignored or already assigned; copy it
                    writer.writerow([row['group_name'], row['folder_name'], \
                    row['folder_value']])

    print('seed created.')
