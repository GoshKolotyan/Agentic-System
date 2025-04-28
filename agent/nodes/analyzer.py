from typing import Dict, Any
from ..utils.state import MessageState
from ..utils.llm import query_llm

def analyze_message(state: MessageState) -> Dict[str, Any]:
    """analyze the user message to determine its intent. """
    user_message = state["messages"][-1].content
    
    prompt = f"""
    Analyze the following user message and determine if it's:
    1. A direct question that should be answered
    2. A request to generate or edit code or text
    
    User message: {user_message}
    
    Return a JSON with the following structure:
    {{
        "intent": "question" | "generation",
        "details": "brief explanation of why you classified it this way"
    }}
    """
    
    result = query_llm(prompt, parse_json=True)
    
    if isinstance(result, dict) and "intent" in result:
        intent = result["intent"]
    else:
        intent = "generation"
    
    return {"intent": intent}