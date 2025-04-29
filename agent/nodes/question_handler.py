import logging
from datetime import datetime

from ..utils.state import MessageState
from ..utils.llm import query_llm
from ..utils.file_utils import FileUtils

def handle_question(state: MessageState) -> MessageState:
    """direct questions and output answers to the terminal"""
    
    user_message = state["messages"][-1].content
    filename = state.get("output_file", None)
    prompt = f"""
    The user has asked the following question:
    {user_message}
    
    Please provide a direct and helpful answer.
    """

    
    answer = query_llm(prompt)
    now = datetime.now()
    timestamp = f"{now.year}{now.month:02d}{now.day:02d}_{now.hour:02d}{now.minute:02d}{now.second:02d}"
    
    #save answer to file
    filename = FileUtils.get_answer_filename(filename=filename)
    FileUtils.write_to_file(filename=filename, content=answer, 
                            is_question=True, user_message=user_message)

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