import csv
import os
import submit_v3 as s

if __name__ == "__main__":
    #use submit_v3's functions to get the source file name
    print('(file to be updated) | ', end='')
    target_file_name = s.get_csv_file()

    #get new file name
    print('(seed file) | ', end='')
    seed_file_name = s.get_csv_file()

    target_groups = {}
    seed_groups = {}

    new_group_count = 0

    try:
        with open(target_file_name) as targetfile:
            reader = csv.DictReader(targetfile)

            for row in reader:
                #get all of the groups currently in the target group
                target_groups[str(row['group_name'])] = ''

        with open(seed_file_name) as seedfile:
            reader = csv.DictReader(seedfile)

            for row in reader:
                #get all of the groups in the seed file, which are NOT already
                #in the target file and which are NOT asks
                if(str(row['group_name']) not in target_groups and \
                int(row['folder_value']) != -2):
                    #passes all criteria. add it and record a new group.
                    seed_groups[str(row['group_name'])] = ''
                    new_group_count += 1

        with open(target_file_name, 'a') as targetfile:

            #get a writer to append group names
            targetwriter = csv.writer(targetfile, delimiter=',')

            with open(seed_file_name) as seedfile:
                reader = csv.DictReader(seedfile)

                for row in reader:
                    #iterate through rows. if they are in seed_groups, they
                    #need to be written to the target file.
                    if(str(row['group_name']) in seed_groups):
                        targetwriter.writerow([row['group_name'], \
                        row['folder_name'], row['folder_value']])


        print('wrote', new_group_count, 'new rows to file', target_file_name)



    except Exception as e:
        print('error merging files')
        print(e)
        exit()
