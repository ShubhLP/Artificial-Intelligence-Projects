from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

schema_get_files_info = types.FunctionDeclaration(
            name="get_files_info",
            description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
            parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                ),
            },
            required=["directory"]
        ),
    )

schema_get_file_content = types.FunctionDeclaration(
    name = 'get_file_content',
    description = "Extract the content of the files in a specified directory relative to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Root directory where the files and folders reside",
                default='.'
            ),
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "Relative path of the file to the root directory"
            ),
        },
        required = ["file_path"]
        )
    )

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Runs Python file in the specified file path relative to its root directory",
    parameters=types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Root directory where the files that you want to run reside",
                default = '.'
            ),
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "File path that points to the file you want to run"
            ),
        },
        required=["file_path"]
    )
)

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes on an existing file",
    parameters=types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Root directory where the files that you want to run reside",
                default = '.'
            ),
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "File path that points to the file you want to wrie on"
            ),
        },
        required=["file_path"]
    )
)

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)

FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(function_call, verbose=False):
    name = function_call.name or ""
    # args = function_call
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # return types.Content(
    #     role = "tool",
    #     parts = [
    #         types.Part.from_function_response(
    #             name = name,
    #             response={"error": f'Unknown function: {name}'},
    #         )
    #     ],
    # )
    func = FUNCTION_MAP.get(name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"}
                )
            ]
        )

    try:
        result = func(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={'result':result}
                )
            ]
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": str(e)}
                )
            ]
        )
