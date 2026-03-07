import subprocess
import shlex
import os

def scan_target(target: str) -> str:
    """
    Performs a fast network scan using Nmap. 
    Returns open ports and service versions. 
    Use this to identify potential attack surfaces on a target.
    """
    try:
        from rich.console import Console
        console = Console()
        console.print(f"\n[bold cyan]🔍 Sera is performing recon on:[/bold cyan] {target}")
        
        # -F: Fast mode - Scan fewer ports than the default scan
        # -sV: Probe open ports to determine service/version info
        # -T4: Faster execution
        command = f"nmap -F -sV -T4 {target}"
        parsed_command = shlex.split(command)
        
        result = subprocess.run(
            parsed_command,
            capture_output=True,
            text=True,
            timeout=60 # Recon can take longer
        )
        
        if result.returncode != 0:
            # If nmap isn't installed, provide a helpful error
            if "not found" in result.stderr.lower():
                return "Error: 'nmap' is not installed on this system. Please install it to use recon tools."
            return f"Error running nmap: {result.stderr}"
            
        return result.stdout.strip() if result.stdout else "Scan completed. No open ports found."
        
    except subprocess.TimeoutExpired:
        return "Error: Recon scan timed out after 60 seconds."
    except Exception as e:
        return f"Error performing recon: {str(e)}"
