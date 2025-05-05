import sys
import logging
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.key_binding import KeyBindings
from rich.logging import RichHandler
from rich.console import Console

# Import state and utilities
from .config import Config
from .utils.state import create_initial_state
from .utils.output_manager import OutputManager
from .helper import GraphManager

# Set up rich console
console = Console()

# Configure rich logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
#for ignoring API logs
logging.getLogger("openai._client").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


kb = KeyBindings()
@kb.add('c-d')  # Ctrl+D to submit
def _(event):
    event.app.exit(result=event.app.current_buffer.text)

@kb.add('escape', 'enter')  # Alt+Enter for new line
def _(event):
    event.app.current_buffer.insert_text('\n')

def main():
    """Main entry point for the application."""
    # Display welcome message
    OutputManager.display_welcome()
    
    # Check if API key is set
    config = Config()
    if not config.check_api_key():
        console.print("[bold red]Error:[/bold red] OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")
        return
    
    try:
        # context manager for graph
        with GraphManager(config) as app:
            console.print("[green]Graph successfully built and initialized[/green]")
            
            while True:
                try:
                    #input with prompt_toolkit
                    console.print("[bold cyan]Enter your message[/bold cyan] (press Alt+Enter for new lines, Ctrl+D to submit):")
                    user_input = prompt(
                        "User message: ",
                        multiline=True,
                        key_bindings=kb,
                    )
                    
                    #empty input avoid
                    if not user_input.strip():
                        console.print("[yellow]Empty input, please try again.[/yellow]")
                        continue
                    
                    initial_state = create_initial_state(user_input)
                    
                    try:
                        app.graph.invoke(initial_state)
                        
                        
                    except Exception as e:
                        console.print(f"[bold red]Error processing input:[/bold red] {str(e)}")
                        logging.error(f"Graph processing error: {str(e)}")
                
                except KeyboardInterrupt:
                    console.print("\n[yellow]Input interrupted. Press Ctrl+C again to exit.[/yellow]")
                    try:
                        prompt("Press Enter to continue or Ctrl+C to exit...")
                    except KeyboardInterrupt:
                        break
    
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Keyboard interrupt detected, shutting down...[/bold yellow]")
    
    except Exception as e:
        console.print(f"\n[bold red]Fatal error:[/bold red] {str(e)}")
        logging.exception("Fatal error in main loop")
    
    finally:
        console.print("[bold green]Exiting agentic system. Goodbye![/bold green]")
        sys.exit(0)