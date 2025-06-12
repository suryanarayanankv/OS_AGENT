import subprocess
import platform


def execute_shell_command(command: str, requires_admin: bool = False):
    """
    Executes a shell command and captures its output.
    ... (rest of your docstring) ...
    """
    current_os = platform.system()
    print(f"--- Inside execute_shell_command ---") # ADD THIS
    print(f"Detected OS: {current_os}") # ADD THIS
    full_command = command

    # Prepend 'sudo' if required and on a Unix-like system
    if requires_admin:
        if current_os in ["Linux", "Darwin"]:  # Darwin is macOS
            full_command = f"sudo {command}"
            print(f"Attempting to execute: {full_command} (You may be prompted for your password)")
        else:
            print("Note: 'requires_admin' flag is set, but 'sudo' is not applicable on Windows.")
            print("You must ensure this script (or the command itself) is run with administrative privileges on Windows.")
            print(f"Attempting to execute: {full_command}")

    print(f"Final command to execute: '{full_command}'") # ADD THIS

    try:
        process = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            check=False  # Don't raise CalledProcessError for non-zero exit codes
        )

        print(f"Subprocess returned: Return Code={process.returncode}") # ADD THIS
        print(f"Subprocess STDOUT: '''{process.stdout.strip()}'''") # ADD THIS (Note: triple quotes to show newlines/empty)
        print(f"Subprocess STDERR: '''{process.stderr.strip()}'''") # ADD THIS

        if process.returncode == 0:
            result = {
                'status': 'success',
                'stdout': process.stdout.strip(),
                'stderr': process.stderr.strip(),
                'returncode': process.returncode,
                'message': f"Command executed successfully on {current_os}."
            }
        else:
            result = {
                'status': 'error',
                'stdout': process.stdout.strip(),
                'stderr': process.stderr.strip(),
                'returncode': process.returncode,
                'message': f"Command failed with exit code {process.returncode} on {current_os}."
            }
        
        print(f"Tool returning result: {result}") # ADD THIS
        return result

    except FileNotFoundError:
        error_result = { # Store error in a variable to print it before returning
            'status': 'error',
            'stdout': '',
            'stderr': f"Command '{command}' not found. Please check the command and your system's PATH.",
            'returncode': -1,
            'message': "Command not found."
        }
        print(f"Tool returning error: {error_result}") # ADD THIS
        return error_result
    except Exception as e:
        error_result = { # Store error in a variable to print it before returning
            'status': 'error',
            'stdout': '',
            'stderr': str(e),
            'returncode': -2,
            'message': f"An unexpected error occurred: {e}"
        }
        print(f"Tool returning unexpected error: {error_result}") # ADD THIS
        return error_result