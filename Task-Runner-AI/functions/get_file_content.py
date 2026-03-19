import os

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        # print(working_dir_abs)
        target_file = os.path.abspath(os.path.normpath(os.path.join(working_dir_abs, file_path)))
        # print(target_file)
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        # print(valid_target_dir)
        if not valid_target_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'


        MAX_CHARS = 10000

        with open(target_file, 'r', encoding='UTF-8') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    
    except Exception as e:
        return f"Error:{e}"