import re
import subprocess
import os

def extract_code(raw_text):
    # Remove markdown code fences
    cleaned_text = re.sub(r"```[\w]*", "", raw_text)
    cleaned_text = cleaned_text.replace("```", "")  # in case any stray backticks remain

    # Remove everything before the first line of code
    split_lines = cleaned_text.splitlines()
    code_lines = []
    code_started = False

    for line in split_lines:
        if re.match(r"^\s*(from |import |class |def |[a-zA-Z0-9_]+\s*=)", line):
            code_started = True
        if code_started:
            code_lines.append(line)

    return "\n".join(code_lines).strip()


def save_code_to_file(code, file_path):
    """Saves the extracted code to a specified file."""
    if not os.path.exists("output/"):
        os.makedirs("output/")    
    file_path = os.path.join("output", file_path)
    with open(file_path, "w") as file:
        file.write(code)
    return file_path


def format_code_with_black(file_path):
    """Formats the Python code in the given file using Black."""
    subprocess.run(["black", file_path], capture_output=True)
