from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown
from typing import Dict, Any, Optional

console = Console()

class OutputManager:
    """
    Manages terminal output formatting using the Rich library.
    Provides consistent, visually appealing output for different response types.
    """
    
    @staticmethod
    def display_response(state: Dict[str, Any]):
        """
        Display a formatted response based on the state.
        
        Args:
            state: Current message state with response information
        """
        # Check if there's an error to display
        if state.get("error"):
            OutputManager.display_error(state)
            return
            
        # Get response components
        response = state.get("response", "")
        intent = state.get("intent", "")
        output_file = state.get("output_file", "")
        
        # Display based on intent type
        if intent == "question":
            OutputManager.display_answer(response)
        elif intent in ["generate_code", "edit_code"]:
            source_code = state.get("source_code", "")
            language = state.get("language", "python")
            OutputManager.display_code_result(response, source_code, language, output_file)
        elif intent in ["generate_text", "edit_text"]:
            source_text = state.get("source_text", "")
            OutputManager.display_text_result(response, source_text, output_file)
        else:
            # Generic response
            OutputManager.display_generic(response)
    
    @staticmethod
    def display_answer(answer: str):
        """Display an answer to a question."""
        panel = Panel(
            Markdown(answer),
            title="Answer",
            border_style="blue",
            padding=(1, 2)
        )
        console.print("\n")
        console.print(panel)
        console.print("\n")
    
    @staticmethod
    def display_code_result(response: str, code: str, language: str, output_file: str):
        """Display code generation/editing result."""
        # Create panel for response summary
        summary_panel = Panel(
            Text(response),
            title="Action Completed",
            border_style="green",
            padding=(1, 2)
        )
        
        # Create syntax-highlighted code panel
        if code:
            try:
                syntax = Syntax(
                    code,
                    language, 
                    theme="monokai",
                    line_numbers=True,
                    word_wrap=True,
                    indent_guides=True
                )
                
                code_panel = Panel(
                    syntax,
                    title=f"Generated {language.capitalize()} Code",
                    border_style="green",
                    padding=(1, 2)
                )
            except Exception:
                # Fallback if syntax highlighting fails
                code_panel = Panel(
                    code,
                    title=f"Generated {language.capitalize()} Code",
                    border_style="green",
                    padding=(1, 2)
                )
        
        # Display all panels
        console.print("\n")
        console.print(summary_panel)
        if code:
            console.print(code_panel)
        if output_file:
            console.print(f"[bold]Output saved to:[/bold] {output_file}")
        console.print("\n")
    
    @staticmethod
    def display_text_result(response: str, text: str, output_file: str):
        """Display text generation/editing result."""
        # Create panel for response summary
        summary_panel = Panel(
            Text(response),
            title="Action Completed",
            border_style="cyan",
            padding=(1, 2)
        )
        
        # Create panel for text preview
        if text:
            text_panel = Panel(
                Markdown(text),
                title="Generated Text (Preview)",
                border_style="cyan",
                padding=(1, 2)
            )
        
        # Display all panels
        console.print("\n")
        console.print(summary_panel)
        if text:
            console.print(text_panel)
        if output_file:
            console.print(f"[bold]Output saved to:[/bold] {output_file}")
        console.print("\n")
    
    @staticmethod
    def display_error(state: Dict[str, Any]):
        """Display error information."""
        error_info = state.get("error", {})
        error_message = state.get("response", "An unknown error occurred")
        error_code = error_info.get("error_code", "UNKNOWN_ERROR")
        error_type = error_info.get("error_type", "Unknown")
        
        # Create error panel
        error_panel = Panel(
            Text(error_message),
            title="Error Occurred",
            border_style="red",
            padding=(1, 2)
        )
        
        # Create details table
        table = Table(show_header=False, box=None)
        table.add_column("Property", style="red")
        table.add_column("Value")
        table.add_row("Error Code", error_code)
        table.add_row("Error Type", error_type)
        
        if "error_message" in error_info:
            technical_msg = error_info["error_message"]
            table.add_row("Technical Details", technical_msg)
        
        # Display error information
        console.print("\n")
        console.print(error_panel)
        console.print(table)
        console.print("\n")
    
    @staticmethod
    def display_generic(message: str):
        """Display a generic message."""
        console.print("\n")
        console.print(Panel(
            Text(message),
            title="Message",
            border_style="blue",
            padding=(1, 2)
        ))
        console.print("\n")
    
    @staticmethod
    def display_welcome():
        """Display a welcome message on startup."""
        welcome_panel = Panel(
            Text("Welcome to the Agentic System! Type your requests or questions to begin."),
            title="Agentic System",
            border_style="cyan",
            padding=(1, 2)
        )
        console.print("\n")
        console.print(welcome_panel)
        console.print("\n")