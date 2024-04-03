import requests
import sys
from io import StringIO


def generate_image(prompt: str, *args, **kwargs):
    print("Generating image")
    url = "https://www.lemonfox.ai/api/generate-images"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "Referer": "https://www.lemonfox.ai/playground/images",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }
    jsonbody = {"prompt": prompt}
    response = requests.post(url, headers=headers, json=jsonbody)
    if response.status_code != 200:
        return "An error occurred while generating the image. Please try again later."

    return str(response.json()[0])


def python_code_runner(code: str, *args, **kwargs):
    print("Running Python code")
    # print(f"Code to run:\n\n{'='*40}\n{code}\n\n{'='*40}")
    try:
        output_capture = StringIO()
        original_stdout = sys.stdout

        lines = code.strip().split("\n")
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() and not lines[i].strip().startswith("#"):
                if not lines[i].strip().startswith("print"):
                    lines[i] = "print(" + lines[i] + ")"
                break

        # Rejoin the modified code
        modified_code = "\n".join(lines)

        try:
            sys.stdout = output_capture
            exec(modified_code)
            captured_output = output_capture.getvalue()

        finally:
            sys.stdout = original_stdout

        return captured_output
    except Exception as e:
        return f"An error occurred: \n\n{e}"
