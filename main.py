import os
import argparse
from dotenv import load_dotenv
from google import genai

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
    args = parser.parse_args()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt
    )

    if response.usage_metadata is None:
        raise RuntimeError("API request failed or returned no usage metadata.")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(response.text)


if __name__ == "__main__":
    main()

