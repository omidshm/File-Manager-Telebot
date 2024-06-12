import os

# Checked
def list_files_in_folder(folder_path, file_format=None):
    files_list = os.listdir(folder_path)
    if file_format:
        files_list = [file for file in files_list if file.endswith(file_format)]
    return files_list

def read_file_content(file_path)-> str:
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def rewrite_file(file_path, new_content):
    with open(file_path, 'w') as file:
        file.write(new_content)
