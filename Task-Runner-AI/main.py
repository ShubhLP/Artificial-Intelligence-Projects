import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

import argparse

# Create parser
parser = argparse.ArgumentParser(
    description = "Take prompt from the user"
)

# add arguments to the parser
parser.add_argument(
    "prompt",
    type = str,
    help = "Enter the prompt for the agent!"
)

parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

# parse the arguments
args = parser.parse_args()

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
# print(api_key)


def main():
    print("Hello from boot-aiagent!")

    MAX_ITERS = 20
    final_response_received = False
    
    for _ in range(MAX_ITERS):
        messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

        response = client.models.generate_content(
        model='gemini-2.5-flash', #contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
        # contents = args.prompt
        contents = messages,
        config = types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
            )
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
            

        # print(response)
        if args.verbose:
            print('User prompt:', args.prompt)
            print('Prompt tokens:', response.usage_metadata.prompt_token_count)
            print('Response tokens:', response.usage_metadata.candidates_token_count)

        function_results = []

        if function_results:
            messages.append(types.Content(role="user", parts=function_results))

        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose = args.verbose)

                if not function_call_result.parts:
                    raise ValueError(f"Function call {function_call.name} returned empty parts")
                
                first_part = function_call_result.parts[0]
                if first_part.function_response is None:
                    raise ValueError(f"Function call {function_call.name} returned no function_response")
                
                if first_part.function_response.response is None:
                    raise ValueError(f"Function call {function_call.name} returned no response data")
                
                actual_result = first_part.function_response.response

                function_results.append(first_part)

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

        else:
            print(response.text)
            final_response_received = True
            break

    if not final_response_received:
        print(f"Error: Maximum iterations ({MAX_ITERATIONS}) reached without a final response.")
        exit(1) 


if __name__ == "__main__":
    main()



# sdk_http_response=HttpResponse(
#   headers=<dict len=11>
# ) =[Candidate(
#   content=Content(
#     parts=[
#       Part(
#         text="""The world of AI is booming,graduate is exciting. By focusing on practical skills, building a compelling portfolio, and staying curious, you can position yourself for success in these hot jobs."""
#       ),
#     ],
#     role='model'
#   ),
#   finish_reason=<FinishReason.STOP: 'STOP'>,
#   index=0
# )] create_time=None model_version='gemini-2.5-flash' prompt_feedback=None response_id='4XGsaezBH5qS-sAPm5HJyQs' usage_metadata=GenerateContentResponseUsageMetadata(
#   candidates_token_count=1713,
#   prompt_token_count=13,
#   prompt_tokens_details=[
#     ModalityTokenCount(
#       modality=<MediaModality.TEXT: 'TEXT'>,
#       token_count=13
#     ),
#   ],
#   thoughts_token_count=1384,
#   total_token_count=3110
# ) automatic_function_calling_history=[] parsed=None

