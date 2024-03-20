import contextlib
import io
import traceback
import openai
import os


class ScriptRunner:
    def __init__(self, api_key_path='openai_api_key.txt'):
        self.api_key = self.read_api_key(api_key_path)

    @staticmethod
    def read_script_to_string(script_filename):
        with open(script_filename, 'r') as file:
            return file.read()

    @staticmethod
    def write_text_to_file(text, file_path):
        with open(file_path, 'w') as file:
            file.write(text)

    def read_api_key(self, api_key_path):
        full_path = os.path.join(os.path.dirname(__file__), "..", "keys", api_key_path)
        with open(full_path, 'r') as file:
            return file.readline().strip()

    def run_python_script_and_check_output(self, script_filename, expected_output_filename):
        script_text = self.read_script_to_string(script_filename)
        with open(expected_output_filename, 'r+') as file:
            expected_output = file.read().strip()

        output_and_error_capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(output_and_error_capture), contextlib.redirect_stderr(
                    output_and_error_capture):
                exec(script_text, globals())
        except Exception:
            output_and_error_capture.write(f"{traceback.format_exc()}")

        actual_output = output_and_error_capture.getvalue().strip()
        is_success = actual_output == expected_output

        self.write_text_to_file(actual_output, 'script_execution_output.txt')

        return is_success, actual_output

    def build_correction_prompt(self, error_message, code_text):
        return (
            "I have a piece of Python code that has some errors. Here's the code:\n\n"
            f"```python\n{code_text}\n```\n\n"
            "And here's the error message I'm getting:\n\n"
            f"```\n{error_message}\n```\n\n"
            "Can you provide the corrected version of the code, give it full not parts? Please format the corrected code like this:\n\n"
            "```python\n# Corrected code starts\n"
            "<corrected_FULL_code>\n"
            "# Corrected code ends\n```"
        )

    def send_prompt_for_correction(self, prompt):
        openai.api_key = self.api_key

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
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

    def attempt_fix_and_run(self, script_filename, expected_output_filename):
        success, output_or_error = self.run_python_script_and_check_output(script_filename, expected_output_filename)
        if not success:
            python_txt = self.read_script_to_string(script_filename)
            prompt = self.build_correction_prompt(output_or_error, python_txt)
            corrected_code = self.send_prompt_for_correction(prompt)
            self.write_text_to_file(corrected_code, script_filename)
        return success


if __name__ == "__main__":
    runner = ScriptRunner('../keys/openai_api_key.txt')
    success = runner.attempt_fix_and_run('../order_files/MyProject_code.py', 'expected_output.txt')
    print(success)
