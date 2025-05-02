import sys
import logging
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.key_binding import KeyBindings

# Import state and utilities
from .config import Config
from .helper import GraphManager
from .utils.state import create_initial_state

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)

kb = KeyBindings()
@kb.add('c-d')  # Ctrl+D to submit
def _(event):
    event.app.exit(result=event.app.current_buffer.text)

@kb.add('escape', 'enter')  # Alt+Enter for newline
def _(event):
    event.app.current_buffer.insert_text('\n')

def main():
    """Main entry point for the application."""
    # Check if API key is set
    config = Config()
    if not config.check_api_key():
        return
    
    try:
        # build the graph
        with GraphManager(config) as app:
            while True:
                # Get user input
                logging.info("Enter your message (press Alt+Enter for new lines, Ctrl+D to submit):")
                user_input = prompt("User message: ", multiline=True, key_bindings=kb,)
                
                if not user_input.strip():
                    logging.warning("Empty input, skipping...")
                    continue
                
                # Initial state with user input
                initial_state = create_initial_state(user_input)

                try:
                    # Process the input through the graph
                    app.invoke(initial_state)
                    app.get_graph()
                except Exception as e:
                    logging.error(f"Error processing input: {e}")
                    print(f"An error occurred while processing your request: {e}")
    
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt detected, shutting down...")
        print("Application terminated. Goodbye!")
        
    # Clean exit
    sys.exit(0)

if __name__ == "__main__":
    main()