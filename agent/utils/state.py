from typing import Optional, Union, TypedDict
from langchain_core.messages import HumanMessage, AIMessage

class MessageState(TypedDict):
    messages: list[Union[HumanMessage, AIMessage]] # messages of the conversation
    intent: Optional[str] # intent of the user
    language: Optional[str] # language of the code
    source_code: Optional[str] # source code of the code
    source_text: Optional[str] # source text of the text
    output_file: Optional[str] # output file of the code
    response: Optional[str] # response of the code

def create_initial_state(user_input: str) -> MessageState:
    return {
        "messages": [HumanMessage(content=user_input)],
        "intent": None,
        "language": None,
        "source_code": None,
        "source_text": None,
        "output_file": None,
        "response": None
    }