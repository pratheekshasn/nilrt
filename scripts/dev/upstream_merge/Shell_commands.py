import subprocess
import shlex

def run_command(command, capture_output=True, shell=False, executable=None):
    """
    Run a shell command and optionally capture the output.
    
    :param command: Shell command as a string.
    :param capture_output: Whether to capture the output.
    :return: (return_code, output) - return code and output string (or None if not captured).
    """
    formatted_command = shlex.split(command)
    print(formatted_command)
    try:
        if capture_output:
            result = subprocess.run(formatted_command,shell=shell, executable=executable, capture_output=True, text=True, check=False)
            return result.returncode, result.stdout.strip()
        else:
            result = subprocess.run(formatted_command,shell=shell, executable=executable, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode, None
    except Exception as e:
        return 1, f"Error running command '{command}': {str(e)}"
