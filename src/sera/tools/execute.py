import subprocess
import shlex

def execute_shell_command(command: str) -> str:
    """
    Executes a shell command locally on the user's machine and returns the output.
    Useful for running network tools like nmap, checking IP addresses, or reading files.
    """
    try:
        from rich.console import Console
        console = Console()
        console.print(f"\n[bold yellow]⚙️ Sera is running command:[/bold yellow] {command}")
        
        # We use shell=False for better security, parsing the command into a list
        # However, many complex chained commands (like pipes) might fail with shell=False.
        # For a more advanced prototype, you might want to consider safer ways to handle pipes.
        parsed_command = shlex.split(command)
        
        result = subprocess.run(
            parsed_command,
            capture_output=True,
            text=True,
            timeout=30 # 30 second timeout so the LLM doesn't hang forever
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]:\n{result.stderr}"
            
        return output.strip() if output else "Command executed successfully with no output."
        
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"
