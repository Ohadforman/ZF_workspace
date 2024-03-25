# run_correction.py

from feedback.close_loop_api import CorrectPy


def main():
    # Initialize the CorrectPy instance with paths to the API key and config file.
    corrector = CorrectPy('openai_api_key.txt', '../Utils/config_correct.json')

    # Specify the path to the Python script you want to correct, the expected output,
    # the path where the script's output will be written, and the maximum number of correction attempts.
    script_path = '../order_files/MyProject_code.py'
    expected_output = 'INFO: No errors or warnings found while generating netlist.'
    max_attempts = 5  # Maximum number of attempts to correct the script

    # Call the attempt_correction method
    corrector.attempt_correction(script_path, expected_output, max_attempts)


if __name__ == "__main__":
    main()


