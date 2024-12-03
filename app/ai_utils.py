import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_code_analysis_prompt(filename, content):
    return f"""
Analyze the following code file "{filename}" for:
- Code style issues
- Bugs
- Performance improvements
- Best practices

Provide the results in JSON format only, without any additional text or explanations. The JSON format should be:
{{
    "issues": [
        {{"type": "<type>", "line": <line>, "description": "<description>", "suggestion": "<suggestion>"}}
    ]
}}

Code:
{content}
"""


def analyze_code_with_openai(filename, content):
    prompt = generate_code_analysis_prompt(filename, content)
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    # Debugging: Print the entire response
    print("OpenAI API response:", response)

    # Extract the assistant's message content
    response_content = response.choices[0].message.content.strip()

    # Attempt to parse the response content as JSON
    try:
        # If the response contains JSON within code blocks, extract it
        if '```json' in response_content:
            json_start = response_content.find('```json') + len('```json')
            json_end = response_content.find('```', json_start)
            json_str = response_content[json_start:json_end].strip()
        else:
            json_str = response_content

        result = json.loads(json_str)
        return result
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        # You can choose to return an empty result or raise an exception
        # For now, we'll raise an exception
        raise Exception("Failed to decode JSON from OpenAI response")

def parse_gpt_response(response_content):
    """
    Parses the GPT response to extract the list of clothing items.
    Assumes the GPT model returns a JSON array of item names.
    """
    try:
        # Find the JSON array in the response
        start_index = response_content.find('[')
        end_index = response_content.find(']', start_index) + 1
        items_json = response_content[start_index:end_index]
        identified_items = json.loads(items_json)
        return identified_items
    except Exception as e:
        print(f"Error parsing GPT response: {e}")
        # If parsing fails, return an empty list
        return []
