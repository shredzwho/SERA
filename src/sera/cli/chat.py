import asyncio
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from sera.llm.client import LLMClient
from sera.core.persona import SERA_SYSTEM_PROMPT

class ChatCLI:
    def __init__(self):
        self.console = Console()
        try:
            self.client = LLMClient()
        except ValueError as e:
            self.console.print(f"[bold red]Error:[/bold red] {e}")
            exit(1)
            
        # Initialize conversation history with the system prompt
        self.messages = [
            {"role": "system", "content": SERA_SYSTEM_PROMPT}
        ]
        
    def welcome_message(self):
        """Prints a cool welcome message."""
        welcome_text = """
        [bold cyan]Sera v0.1 - AI Hacking Assistant Prototype[/bold cyan]
        
        [yellow]Type 'exit' or 'quit' to end the session.[/yellow]
        [yellow]Type 'clear' to reset the conversation context.[/yellow]
        """
        self.console.print(Panel(welcome_text, title="Terminal", border_style="cyan"))
        
    async def chat_loop(self):
        """The main interactive chat loop."""
        self.welcome_message()
        
        while True:
            # Get user input
            try:
                user_input = self.console.input("\n[bold green]User ❯ [/bold green] ")
            except (KeyboardInterrupt, EOFError):
                 self.console.print("\n[dim]Exiting...[/dim]")
                 break

            if not user_input.strip():
                continue
                
            command = user_input.strip().lower()
            if command in ['exit', 'quit']:
                self.console.print("[dim]Goodbye.[/dim]")
                break
            elif command == 'clear':
                self.messages = [{"role": "system", "content": SERA_SYSTEM_PROMPT}]
                self.console.print("[dim]Context cleared.[/dim]")
                continue

            # Add user message to history
            self.messages.append({"role": "user", "content": user_input})
            
            # Show a spinner while generating
            with self.console.status("[bold cyan]Sera is thinking...", spinner="dots"):
                response_text = await self.client.generate_response(self.messages)
            
            # Print response
            self.console.print("\n[bold magenta]Sera ❯[/bold magenta]")
            self.console.print(Markdown(response_text))
            
            # Add assistant message to history
            self.messages.append({"role": "assistant", "content": response_text})

async def start_chat():
    """Async entry point for the chat CLI."""
    cli = ChatCLI()
    await cli.chat_loop()

def run_chat():
    """Entry point wrapper for the async chat loop."""
    asyncio.run(start_chat())
    
if __name__ == "__main__":
    run_chat()
