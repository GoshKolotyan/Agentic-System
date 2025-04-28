import logging
from ..utils.state import MessageState
from ..utils.llm import query_llm

def handle_question(state: MessageState) -> MessageState:
    """direct questions and output answers to the terminal"""
    
    user_message = state["messages"][-1].content
    
    prompt = f"""
    The user has asked the following question:
    {user_message}
    
    Please provide a direct and helpful answer.
    """
    
    answer = query_llm(prompt)
    
    #summary for logging
    summary = answer[:100] + "..." if len(answer) > 100 else answer
   
    #logging     
    logging.info("ANSWER OF QUESTION:")
    logging.info(f"{answer}")

    # Update state
    return {
        **state,
        "response": f"I've answered your question: {summary}"
    }