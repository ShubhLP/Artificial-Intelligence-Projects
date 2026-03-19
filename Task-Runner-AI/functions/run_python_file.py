import os
from pathlib import Path
import subprocess

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.normpath(os.path.join(working_dir_abs, file_path)))

    # print(working_dir_abs)
    # print(target_file)

    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    # print(valid_target_dir)
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
     
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    absolute_target_file_path = Path(target_file)

    if not absolute_target_file_path.is_file():
        return f'Error: "{file_path}" does not exist'
    # print(absolute_target_file_path)
    if absolute_target_file_path.suffix != '.py':
        return f'Error: "{file_path}" is not a Python file'
    
    os.makedirs(os.path.dirname(target_file), exist_ok = True)
    
    command = ["python", str(absolute_target_file_path)]

    if args:
        command.extend(args)

    try:
        result = subprocess.run(command, cwd = working_dir_abs, capture_output = True, text = True, timeout = 30)
        # return result.stdout + result.stderr
        output = ''

        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        
        if not result.stdout and not result.stderr:
            output += "No output produced"
        
        else:
            if result.stdout:
                output += f'STDOUT: {result.stdout}'
            if result.stderr:
                output += f'STDERR: {result.stderr}'
        
        return output.strip()
    
    except Exception as e:
        return 'Error: executing Python file: {e}'
    
# run_python_file('calculator', 'pkg/calculator')