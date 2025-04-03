import subprocess
import shlex
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='mylog.log', level=logging.INFO)

def run_command(command, capture_output=True):
    """
    Run a shell command and optionally capture the output.
    
    :param command: Shell command as a string.
    :param capture_output: Whether to capture the output.
    :return: (return_code, output) - return code and output string (or None if not captured).
    """
    print(command)
    logger.info("Running command: %s", command)
    formatted_command = shlex.split(command)
    try:
        if capture_output:
            result = subprocess.run(formatted_command, capture_output=True, text=True, check=False)
            logger.info("Command output: %s", result.stdout.strip() + result.stderr.strip())
            return result.returncode, result.stdout.strip() + result.stderr.strip()
        else:
            result = subprocess.run(formatted_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info("Command output: %s", result.stdout.strip() + result.stderr.strip())
            return result.returncode, None
    except Exception as e:
        logger.info("Exception running command: %s", str(e))
        return 1, f"Error running command '{command}': {str(e)}"
    
def execute(command):
    """
    Execute a command and yield its output line by line in real-time.

    :param command: Command to execute as a string.
    :yield: Lines of output from the command.
    """
    print(command)
    logger.info("Running command: %s", command)
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True 
        )

        retval = ""
        while True:
            nextline = process.stdout.readline()
            retval += nextline
            if nextline == '' and process.poll() is not None:
                break
            sys.stdout.write(nextline)
            sys.stdout.flush()
        
        logger.info("Command output: %s", retval)
        return process.returncode, retval
    except Exception as e:
        return 1, f"Error running command '{command}': {str(e)}"