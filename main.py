#!/usr/bin/env python3
import os
import sys

# Add the src directory to the Python path so we can import sera
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
import argparse
from sera.cli.chat import start_chat
from sera.api import serve_server

async def main():
    parser = argparse.ArgumentParser(description="Sera: AI Hacking Assistant")
    parser.add_argument("--server", action="store_true", help="Start the Sera Shadow API server")
    parser.add_argument("--port", type=int, default=8000, help="Port for the API server")
    
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()
    
    if args.server:
        print(f"[*] Initializing Sera Shadow Neural Interface on port {args.port}...")
        await serve_server(port=args.port)
    else:
        # Default to CLI mode
        await start_chat()

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Session Terminated.")
        sys.exit(0)
