import openai
import os
import json
import subprocess


class CorrectPy:
    def __init__(self, api_key_path: str = 'openai_api_key.txt',
                 config_path: str = '../Utils/config_correct.json') -> None:
        """
        Initializes the ScriptRunner with specified API key and configuration file paths.

        :param api_key_path: A string path to the OpenAI API key file.
        :param config_path: A string path to the configuration JSON file.
        """
        self.api_key = self.read_api_key(api_key_path)
        self.config = self.load_config(config_path)

    @staticmethod
    def read_script_to_string(script_filename: str) -> str:
        """
        Reads and returns the content of a Python script file as a string.

        :param script_filename: The file path of the script to read.
        :return: The content of the script as a string.
        """
        with open(script_filename, 'r') as file:
            return file.read()

    @staticmethod
    def read_api_key(api_key_path: str) -> str:
        """
        Reads the OpenAI API key from a file.

        :param api_key_path: The file path of the API key.
        :return: The API key as a string.
        """
        full_path = os.path.join(os.path.dirname(__file__), "..", "keys", api_key_path)
        with open(full_path, 'r') as file:
            return file.readline().strip()

    @staticmethod
    def load_config(config_path: str) -> dict:
        """
        Loads the JSON configuration file.

        :param config_path: The file path of the configuration file.
        :return: A dictionary representing the loaded configuration.
        """
        with open(config_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def write_text_to_file(text: str, file_path: str) -> None:
        """
        Writes the provided text to a specified file, overwriting its contents if it already exists,
        or creating it if it does not.

        :param text: The text to be written to the file.
        :param file_path: The full path to the file where the text will be written.
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)

    @staticmethod
    def run_python_script_and_get_combined_output(script_path: str) -> str:
        """
        Executes a Python script and returns a single string containing both its standard output and standard error.

        :param script_path: The path to the Python script file to be executed.
        :return: A string containing the combined standard output and standard error of the script.
        """
        try:
            completed_process = subprocess.run(["python", script_path], capture_output=True, text=True, check=True)
            return completed_process.stdout + completed_process.stderr
        except subprocess.CalledProcessError as e:
            return e.stdout + e.stderr

    def build_correction_prompt(self, error_message: str, code_text: str) -> str:
        """
        Constructs a correction prompt for OpenAI based on an error message and the original code.

        :param error_message: The error message obtained from running the code.
        :param code_text: The original source code that produced the error.
        :return: A string formatted as a prompt for OpenAI.
        """
        cfg = self.config['correction_prompt']
        return (
            f"{cfg['introduction']}"
            f"```python\n{code_text}\n```\n\n"
            f"{cfg['error_intro']}"
            f"```\n{error_message}\n```\n\n"
            f"{cfg['correction_request']}"
            "```python\n# Corrected code starts\n"
            "<corrected_FULL_code>\n"
            "# Corrected code ends\n```"
        )

    def send_prompt_for_correction(self, prompt: str) -> str:
        """
        Sends a correction prompt to OpenAI and retrieves a suggestion for corrected code.

        :param prompt: The prompt to send to OpenAI for correction.
        :return: A string containing the corrected code suggested by OpenAI.
        """
        openai.api_key = self.api_key
        api_config = self.config['api']

        try:
            response = openai.ChatCompletion.create(
                model=api_config['model'],
                messages=[{"role": "system", "content": prompt}],
            )
            response_text = response.choices[0].message['content'] if response.choices else "No correction found."
            if "# Corrected code starts" in response_text:
                corrected_code = response_text.split("# Corrected code starts")[1].split("# Corrected code ends")[
                    0].strip()
            else:
                corrected_code = response_text.strip()
            return corrected_code
        except Exception as e:
            return f"An error occurred: {e}"


if __name__ == "__main__":
    corpy = CorrectPy('openai_api_key.txt', '../Utils/config_correct.json')
    script_path = '../order_files/MyProject_code.py'
    expected_output = 'INFO: No errors or warnings found while generating netlist.'
    output_path = 'script_execution_output.txt'
    max_attempts = 2
    attempt = 0
    success = False

    while attempt < max_attempts and not success:
        # Step 1: Run the Python script and get its output
        output = corpy.run_python_script_and_get_combined_output(script_path)

        # Step 3: Compare the output file with the expected output file
        # print("output:", output.strip().split(), "expected:", expected_output.strip().split())
        if output.strip().split() == expected_output.strip().split():
            print("Success: The script's output matches the expected output.")
            success = True
            break
        else:
            print("The script's output does not match the expected output. Attempting correction...")
            # Step 4: Read the script and build a correction prompt
            script_text = corpy.read_script_to_string(script_path)
            correction_prompt = corpy.build_correction_prompt(output, script_text)
            # Step 5: Send the correction prompt and receive corrected code
            corrected_code = corpy.send_prompt_for_correction(correction_prompt)
            # Step 6: Write the corrected code back to the script file
            corpy.write_text_to_file(corrected_code, script_path)
            attempt += 1
    if not success:
        print(f"Failed to correct the script after {max_attempts} attempts.")
