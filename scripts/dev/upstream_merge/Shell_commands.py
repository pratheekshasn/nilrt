import subprocess
import shlex
import sys

def run_command(command, capture_output=True):
    """
    Run a shell command and optionally capture the output.
    
    :param command: Shell command as a string.
    :param capture_output: Whether to capture the output.
    :return: (return_code, output) - return code and output string (or None if not captured).
    """
    formatted_command = shlex.split(command)
    try:
        if capture_output:
            result = subprocess.run(formatted_command, capture_output=True, text=True, check=False)
            return result.returncode, result.stdout.strip()
        else:
            result = subprocess.run(formatted_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode, None
    except Exception as e:
        return 1, f"Error running command '{command}': {str(e)}"
    
def execute(command):
    """
    Execute a command and yield its output line by line in real-time.

    :param command: Command to execute as a string.
    :yield: Lines of output from the command.
    """
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True 
        )

        while True:
            nextline = process.stdout.readline()
            if nextline == '' and process.poll() is not None:
                break
            sys.stdout.write(nextline)
            sys.stdout.flush()

        return process.returncode, process.communicate()[0]
    except Exception as e:
        return 1, f"Error running command '{command}': {str(e)}"