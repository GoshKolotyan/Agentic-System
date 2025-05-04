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

    #save answer to file
    filename = FileUtils.get_answer_filename(filename=filename)
    FileUtils.write_to_file(filename=filename, content=answer, 
                            is_question=True, user_message=user_message)

    #summary for logging
    # summary = answer[:100] + "..." if len(answer) > 100 else answer # removed summry as it was not needed
   
    #logging     
    # logging.info(f"ANSWER OF QUESTION: {answer}")
    # logging.info(f"{answer}")
    # print(f"{answer}")

    # Update state
    return {
        **state,
        "response": f"I've answered your question: {answer}"
    }