#FILE RENAMER
#Renames all files as 1.jpg, 2.jpg, 3.jpg... etc. 
#Set folder to name of folder you want to rename
#Make sure you're in the right directory

import os
# Specify the folder containing the files
folder = 'images'
# Get a list of all files in the folder
files = os.listdir(folder)
count = 1
# Loop through each file
for filename in files:
    if f"{filename}.jpg" in files:
        duplicate_path = os.path.join(folder, filename)
        # Remove the duplicate file (the one without .jpg)
        os.remove(duplicate_path)
    # Get the full file path
    old_path = os.path.join(folder, filename)
    # Skip if it's not a file or already has ".jpg"
    if not os.path.isfile(old_path) or filename.endswith('.jpg'):
        continue
    # Create the new file name by adding ".jpg" to the existing name
    new_name = f"{count}.jpg"
    
    new_path = os.path.join(folder, new_name)

    # Rename the file
    os.rename(old_path, new_path)
    count += 1

print("Renaming completed!")
