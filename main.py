#!/usr/bin/env python3
import os
import sys

# Add the src directory to the Python path so we can import sera
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
from sera.cli.chat import run_chat

def main():
    """
    Main entry point for the Sera prototype.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Run the chat CLI
    run_chat()

if __name__ == "__main__":
    main()
