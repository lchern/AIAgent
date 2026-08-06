import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("ERROR: api_key is not found!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

def main():
    for _ in range(20):
        completion = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        if completion.usage is None:
            raise RuntimeError("ERROR: API request failed")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {completion.usage.prompt_tokens}")
            print(f"Response tokens: {completion.usage.completion_tokens}")

        message = completion.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if not result_message.get("content"):
                    raise Exception("Error: message content is blank")
                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(message.content)
            sys.exit(0)



    print(f"Error: maximum number of iterations reached; no final response is given")
    sys.exit(1)

if __name__ == "__main__":
    main()
