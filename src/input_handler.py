import signal
import sys
import os
# import readline
from logging import getLogger

logger = getLogger(__name__)


HISTORY_FILE = os.path.expanduser('~/.agentic_history')
HISTORY_LENGTH = 1000

def init_history():
    """Initialize command history."""
    pass 
    # if os.path.exists(HISTORY_FILE):
    #     readline.read_history_file(HISTORY_FILE)
    # readline.set_history_length(HISTORY_LENGTH)
    
def save_history():
    """Save command history to file."""
    pass 
    # readline.write_history_file(HISTORY_FILE)
    

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    logger.info("Exiting program. Goodbye!")
    save_history()
    sys.exit(0)

def get_user_input():
    """
    Capture user input from terminal with command history support.
    Returns the user's message as a string.
    """
    # Initialize command history
    init_history()

    
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Display prompt and get input
        user_input = input("\nAgentic> ")
        
        # Basic validation - check if input is empty
        if not user_input.strip():
            logger.info("Input cannot be empty. Please try again.")
            return get_user_input()  # Recursive call to get valid input
            
        return user_input.strip()
        
    except EOFError:
        # Handle Ctrl+D
        logger.info("\nEOF detected. Exiting program.")
        save_history()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error capturing input: {e}")
        return get_user_input()  # Try again on error