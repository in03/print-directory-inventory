import os, sys
import time
import csv

import win32api
import humanfriendly


name_blacklist = [
    "Rendered - ",
    "$"
]

type_whitelist = [
    ".mp4",".mov",".mxf",".dcp",".mkv",".avi"
    ".wav",".mp3",".aac",
    ".png",".jpg",".jpeg",".psd",".psb",".exr",".afphoto"
    ".prproj",".prproj",".fcpxml",".xml",".edl",".aep",".fcpbundle"
    ".ahk",".py",".ipynb",".json",".js",".html",".bat",".cmd",".exe",
    ".doc",".docx",".pdf",".txt",".rtf",".log",".md",".ini",
    ".zip",".7z",".rar",".tar.gz"
]


######## Functions ########

def input_confirm(conf_msg):
    user_response = input(conf_msg + "\n")
    if "y" in user_response.lower():
        print("Continuing")
    elif "n" in user_response.lower():
        print("Aborting")
        sys.exit(2)
    else:
        print(f"Invalid response, \"{user_response.lower()}\". Try again.")
        input_confirm(conf_msg)

def write_to_csv(path, values):
    # write CSV file
    with open(out_file, "a", newline = '', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter =",")

        to_write = []
        to_write.append(path)
        to_write.extend(values)
        writer.writerow(to_write)

    print(to_write, end="                                                                                 \r", flush =True)


def get_attributes(name):

    attributes = []
    
    try:
        create_time = str(time.strftime('%d/%m/%Y', time.gmtime(os.path.getctime(os.path.join(root, name)))))
    except:
        create_time = "N/A"
    try:
        mod_time = str(time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(os.path.join(root, name)))))
    except:
        mod_time = "N/A"
    try:
        acc_time = str(time.strftime('%d/%m/%Y', time.gmtime(os.path.getatime(os.path.join(root, name)))))
    except:
        acc_time = "N/A"
    try:
        size = humanfriendly.format_size(os.path.getsize(os.path.join(root, name)))
    except:
        size = "N/A"
    
    attributes.append(create_time)
    attributes.append(mod_time)
    attributes.append(acc_time)
    attributes.append(size)
      
    printable_path = os.path.join(root, name)
    write_to_csv(printable_path, attributes)


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

    def check_scan_path(cwd):
        # Check path before change
        if os.path.exists(cwd):
            return cwd
        if os.path.exists(f"{cwd}:"):
            return (f"{cwd}:")
        else:
            return None

    cwd = check_scan_path(cwd)
    if not cwd: 
        print(f"Path \"{cwd}\" is invalid")
        sys.exit(1)

    # Get output file name
    # Save volume name
    try:
        volume = win32api.GetVolumeInformation(cwd)
        out_file = (f"{volume[0]}_drive_inventory.csv")
    except:
        out_file = ("drive_inventory.csv")

    out_file_path = os.path.join(cwd, out_file)
    if os.path.exists(out_file_path):
        input_confirm(f"Output file, \"{out_file}\" already exists. Overwrite? yes/no")
        

    try:
        # Change the current working Directory    
        os.chdir(cwd)
        print(f"Changed working directory to \"{cwd}\"")
    except OSError:
        print("Can't change the Current Working Directory")

    



    # Scan path
    wrong_type = []
    blacklisted_file= []

    file_count = 0
    dir_count = 0

    print("PATH, DATE CREATED, DATE LAST MODIFIED, DATE LAST ACCESSED ")
    for root, dirs, files in os.walk(cwd, topdown=False):
        for dir in dirs:
            get_attributes(dir)
            dir_count +=1
        for file in files:
            for name in name_blacklist:
                if name not in os.path.basename(file):
                    if os.path.splitext(file)[1] in type_whitelist:
                        get_attributes(file)
                        file_count +=1
                    else:
                        wrong_type.append(file)
                else:
                    blacklisted_file.append(file)

    write_to_csv("Directory Count", dir_count)
    write_to_csv("File Count", file_count)

    print('')
    print(f"Finished scanning {dir_count} directories and {file_count} files.")
    if len(blacklisted_file) > 0:
        print(f"{len(blacklisted_file)} files were skipped because they matched the blacklist")
        print(f"{len(wrong_type)} files were skipped because of their filetype")
    input("Press Enter to exit...")
    sys.exit(0)
