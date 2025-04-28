import logging
from ..utils.state import MessageState

def generate_response(state: MessageState) -> MessageState:
    """info about what was done. """
    response = state.get("response", "Processed your request")
    
    # Print to terminal with formatting
    logging.info("ACTION COMPLETED:")
    # logging.info(f"{response}")
    
    # If there's an output file, print its path
    if "output_file" in state and state["output_file"]:
        logging.info(f"\nOutput saved to: {state['output_file']}")
        
    return state