from ..utils.state import MessageState

def primary_router(state: MessageState) -> str:
    """primary router that determines the next node based on the intent."""
    if state.get("intent") == "question":
        return "handle_question"
    elif state.get("intent") == "generation":
        return "classify_intent"
    else:
        return "generate_response"

def intent_router(state: MessageState) -> str:
    """Intent router that determines the specific processing node."""
    specific_intent = state.get("intent")
    
    if specific_intent == "generate_code":
        return "generate_code"
    elif specific_intent == "edit_code":
        return "edit_code"
    elif specific_intent == "generate_text":
        return "generate_text"
    elif specific_intent == "edit_text":
        return "edit_text"
    else:
        return "generate_response"