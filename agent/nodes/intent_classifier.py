from typing import Any
from ..utils.state import MessageState
from ..utils.llm import query_llm

def classify_intent(state: MessageState) -> dict[str, Any]:
    """
    Classify what type of generation or editing is requested.
    This node determines the specific intent from:
    1. generate_code: User wants to generate new code
    2. edit_code: User wants to edit existing code
    3. generate_text: User wants to generate free text
    4. edit_text: User wants to edit existing text
    """
    user_message = state["messages"][-1].content
    
    prompt = f"""
    Analyze the following user request for generation or editing:
    {user_message}
    
    Determine the specific intent from these categories:
    1. generate_code: User wants to generate new code
    2. edit_code: User wants to edit existing code
    3. generate_text: User wants to generate free text
    4. edit_text: User wants to edit existing text
    
    If code-related, also determine the programming language.
    
    Return a JSON with the following structure:
    {{
        "specific_intent": "generate_code" | "edit_code" | "generate_text" | "edit_text",
        "language": "python" | "java" | "cpp" | "javascript" | etc.,
        "details": "brief explanation of why you classified it this way"
    }}
    """
    
    result = query_llm(prompt, parse_json=True)
    
    updates = {}
    
    if isinstance(result, dict):
        if "specific_intent" in result:
            updates["intent"] = result["specific_intent"]
        elif "intent" in result:
            updates["intent"] = result["intent"]
        
        if "language" in result and result["language"]:
            updates["language"] = result["language"]
    
    return updates