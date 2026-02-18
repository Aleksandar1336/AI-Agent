import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError(
        "API_KEY environment variable not found. "
        "Please set it before running the application."
    )

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    for _ in range(20):  # iteration safety limit
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
                temperature=0,
            ),
        )

        if response.usage_metadata is None:
            raise RuntimeError("API request failed or returned no usage metadata.")

        # ✅ Add model responses to conversation history
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        function_responses = []

        # ✅ Handle tool calls
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(
                    function_call,
                    verbose=args.verbose,
                )

                if not function_call_result.parts:
                    raise Exception("Function call result has no parts")

                function_response = function_call_result.parts[0].function_response
                if function_response is None:
                    raise Exception("Function response is None")

                if function_response.response is None:
                    raise Exception("Function response payload is None")

                function_responses.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_response.response}")

            # ✅ Feed tool results back into conversation
            messages.append(
                types.Content(
                    role="user",
                    parts=function_responses,
                )
            )

        else:
            # ✅ Final response reached
            print("Final response:")
            print(response.text)
            return

    # ❌ If loop exits without final answer
    print("Agent stopped after reaching maximum iterations.")
    exit(1)


if __name__ == "__main__":
    main()

