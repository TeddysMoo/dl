# Written by Dylan Tuminelli using ChatGPT
# Fixer! - Changes every file in a selected folder to the desired file type. 
# Version 1.0 - 5/31/2023
import os

def main():
    filetype = input("Enter the desired filetype: ")
    folder_path = input("Enter your folder's path: ")

    for filename in os.listdir(folder_path):
        
                new_filename = f"{filename}{filetype}"       
                os.rename(
                    os.path.join(folder_path, filename),
                    os.path.join(folder_path, new_filename)
                )
        
    print("File renaming completed.")

if __name__ == "__main__":
    main()
