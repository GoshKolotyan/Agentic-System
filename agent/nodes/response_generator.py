import logging
from ..utils.state import MessageState
from ..utils.output_manager import OutputManager

def generate_response(state: MessageState) -> MessageState:
    """
    Generate a final response and display it to the user.
    This node is the terminal node for all processing paths.
    """
    # Set default response if not present
    if "response" not in state or not state["response"]:
        state["response"] = "Processed your request"
    
    # Log the final state for debugging
    logging.debug(f"Final state: {state}")
    
    # Display formatted response in terminal
    OutputManager.display_response(state)
    
    # If there's an output file, log its path for reference
    # if "output_file" in state and state["output_file"]:
    #     logging.info(f"Output saved to: {state['output_file']}")
    
    return state