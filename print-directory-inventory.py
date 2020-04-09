import os, sys
import time
import csv

import win32api


######## Functions ########
def store_path(name):

    # Get modification time
    try:
        mod_time = str(time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(os.path.join(root, name)))))
    except:
        mod_time = "N/A"     
    printable_path = os.path.join(root, name)
    write_to_csv(printable_path, mod_time)

def write_to_csv(key, value):
    # write CSV file
    with open(out_file, "a", newline = '', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter =",")
        writer.writerow([key, value])
    print(key + " | " + value)

###########################


if __name__ == "__main__":
    # Get path to scan
    # Specify if not supplied
    if len(sys.argv) == 1:
        cwd = input("Enter path to scan:\n")

    # Too many paths

    elif len(sys.argv) > 2:
        print("Can only scan one path at a time! Aborting.")
        sys.exit(1)

    # Path supplied
    else:
        cwd = sys.argv[1]

    # Check path before change
    if not os.path.exists(cwd):
        print(f"Path \"{cwd}\" is invalid")
        sys.exit(1)

    # Get output file name
    # Save volume name
    try:
        volume = win32api.GetVolumeInformation(cwd)
        out_file = (f"{volume[0]}_drive_inventory.csv")
    except:
        out_file = ("drive_inventory.csv")


    try:
        # Change the current working Directory    
        os.chdir(cwd)
        print(f"Changed working directory to \"{cwd}\"")
    except OSError:
        print("Can't change the Current Working Directory")    

    # Scan path
    file_count = 0
    dir_count = 0
    for root, dirs, files in os.walk(cwd, topdown=False):
        for dir in dirs:
            store_path(dir)
            dir_count +=1
        for file in files:
            store_path(file)
            file_count +=1

    write_to_csv("Directory Count", dir_count)
    write_to_csv("File Count", file_count)

    print(f"Finished scanning {dir_count} directories and {file_count} files.")
    input("Press Enter to exit...")
    sys.exit(0)
