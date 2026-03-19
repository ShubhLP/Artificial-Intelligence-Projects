import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(os.path.join(working_directory))
        target_dir = os.path.abspath(os.path.normpath(os.path.join(working_directory, directory)))
        
        # print(working_dir_abs)
        # print(target_dir)
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        # print(target_dir, valid_target_dir)
        file_list = os.listdir(target_dir)
        # print(file_list)
        
        results = []
        for f in file_list:
            # print(f, os.path.exists(os.path.join(target_dir, f)))
            file_path = os.path.join(target_dir, f)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            # print(f'-{f}:', 'file_size=', file_size, 'is_dir=', is_dir)
            results.append(
                    f"- {f}: file_size={file_size} bytes, is_dir={is_dir}"
                )
        return "\n".join(results)
    except Exception as e:
        return f'Error: {e}'