import contextlib
import io
import traceback
import openai
import os

def read_script_to_string(script_filename):
    """
    Reads the content of a Python script file and returns it as a string.
    """
    with open(script_filename, 'r') as file:
        return file.read()


def run_python_script_and_check_output(script_filename, expected_output_filename):
    """
    Executes a Python script, compares its output to the expected output,
    and returns whether the execution was successful and the actual output or error message.
    """
    script_text = read_script_to_string(script_filename)

    with open(expected_output_filename, 'r') as file:
        expected_output = file.read().strip()

    output_and_error_capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_and_error_capture), contextlib.redirect_stderr(output_and_error_capture):
            exec(script_text, globals())
    except Exception:
        output_and_error_capture.write(f"{traceback.format_exc()}")

    actual_output = output_and_error_capture.getvalue().strip()
    is_success = actual_output == expected_output

    with open('script_execution_output.txt', 'w') as file:
        file.write(f"{actual_output}")

    return is_success, actual_output if not is_success else ''


def build_correction_prompt(error_message: str, code_text: str) -> str:
    """
    Builds a prompt asking for corrections to a given piece of code based on an error message.

    Parameters:
    error_message (str): The error message received when the code was executed.
    code_text (str): The actual code text that needs correction.

    Returns:
    str: A prompt for the OpenAI API formatted to ask for code corrections.
    """
    prompt = (
        "I have a piece of Python code that has some errors. Here's the code:\n\n"
        f"```python\n{code_text}\n```\n\n"
        "And here's the error message I'm getting:\n\n"
        f"```\n{error_message}\n```\n\n"
        "Can you provide the corrected version of the code, give it full not parts? Please format the corrected code like this:\n\n"
        "```python\n# Corrected code starts\n"
        "<corrected_FULL_code>\n"
        "# Corrected code ends\n```"

    )

    return prompt


def send_prompt_for_correction(api_key: str, prompt: str) -> str:
    """
    Sends a prompt to the OpenAI API using GPT-3.5-turbo model and extracts the corrected code from the response.

    Parameters:
    - api_key (str): The OpenAI API key.
    - prompt (str): The prompt asking for code corrections.

    Returns:
    - str: The corrected Python code ready to be executed, or an error message.
    """
    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
        )
        response_text = response.choices[0].message['content'] if response.choices else "No correction found."
        # Extract only the corrected code block
        # Assumes that the response will contain a phrase indicating the start of corrected code.
        if "# Corrected code starts" in response_text:
            corrected_code = response_text.split("# Corrected code starts")[1].split("# Corrected code ends")[0].strip()
        else:
            corrected_code = response_text.strip()  # Fallback if no specific start phrase is in the response

        return corrected_code
    except Exception as e:
        return f"An error occurred: {e}"


def read_api_key():
        # Assuming the API key is stored in 'openai_api_key.txt' within a 'keys' folder
        # located one directory above the current file's directory
        api_key_path = os.path.join(os.path.dirname(__file__), "..", "keys", "openai_api_key.txt")
        with open(api_key_path, 'r') as file:
            return file.readline().strip()


def write_text_to_file(text, file_path):
    """
    Writes given text to a file at the specified file path.

    Parameters:
    text (str): Text to be written to the file.
    file_path (str): Path to the file where the text will be written.
    """
    with open(file_path, 'w') as file:
        file.write(text)


if __name__ == "__main__":

    script_filename = '../order_files/MyProject_code.py'  # Update this path
    expected_output_filename = 'expected_output.txt'  # Update this path
    success, output_or_error = run_python_script_and_check_output(script_filename, expected_output_filename)
    python_txt = read_script_to_string(script_filename)
    prompt = build_correction_prompt(output_or_error, python_txt)
    api_key = read_api_key()
    print(f"Was the execution successful? {'Yes' if success else 'No'}")
    if not success:
        print("Error or Output:")
        print(output_or_error, '\n', '\n', '\n')
        print(build_correction_prompt(output_or_error, python_txt))
        correct_msg = send_prompt_for_correction(api_key, prompt)
        write_text_to_file(correct_msg, script_filename)
    if success:
        print('code with no warnings')