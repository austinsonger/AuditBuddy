import os

def list_files(startpath):
    with open('file_list.txt', 'w') as f:
        for root, dirs, files in os.walk(startpath):
            for filename in files:
                f.write(os.path.join(root, filename) + '\n')

# Change the directory path as needed
directory_path = '/Users/austin-songer/code/1/AuditAlly'
list_files(directory_path)
