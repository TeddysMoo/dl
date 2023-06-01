import os

def main():
    filetype = input("Enter the filetype: ")
    folder_path = input("Enter the folder path: ")

    for filename in os.listdir(folder_path):
        
                new_filename = f"{filename}{filetype}"       
                os.rename(
                    os.path.join(folder_path, filename),
                    os.path.join(folder_path, new_filename)
                )
        
    print("File renaming completed.")

if __name__ == "__main__":
    main()
