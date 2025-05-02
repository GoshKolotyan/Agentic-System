import signal
import logging

from langgraph.graph import StateGraph, END

# Import state and utilities
from .utils.state import MessageState
from .utils.router import primary_router, intent_router

# Import nodes 
from .nodes.analyzer import analyze_message
from .nodes.question_handler import handle_question
from .nodes.intent_classifier import classify_intent
from .nodes.code_processor import generate_code, edit_code
from .nodes.text_processor import generate_text, edit_text
from .nodes.response_generator import generate_response

shutdown_requested = False


def signal_handler(sig, frame):
    global shutdown_requested
    logging.info("Shutdown signal received, completing current operation...")
    shutdown_requested = True

def build_graph():
    """LangGraph state machine."""
    # init of graph
    workflow = StateGraph(MessageState)
    
    # adding nodes
    workflow.add_node("analyze_message", analyze_message)
    workflow.add_node("handle_question", handle_question)
    workflow.add_node("classify_intent", classify_intent)
    workflow.add_node("generate_code", generate_code)
    workflow.add_node("edit_code", edit_code)
    workflow.add_node("generate_text", generate_text)
    workflow.add_node("edit_text", edit_text)
    workflow.add_node("generate_response", generate_response)
    
    # adding edges for praph
    workflow.set_entry_point("analyze_message")
    
    # Add conditional edges for the primary router
    workflow.add_conditional_edges(
        "analyze_message",
        primary_router,
        {
            "handle_question": "handle_question",
            "classify_intent": "classify_intent",
            "generate_response": "generate_response"
        }
    )
    
    # Add edge from question handler to response generator
    workflow.add_edge("handle_question", "generate_response")
    
    # Add conditional edges for the intent router
    workflow.add_conditional_edges(
        "classify_intent",
        intent_router,
        {
            "generate_code": "generate_code",
            "edit_code": "edit_code",
            "generate_text": "generate_text",
            "edit_text": "edit_text",
            "generate_response": "generate_response"
        }
    )
    
    # edges from processors to response generator
    workflow.add_edge("generate_code", "generate_response")
    workflow.add_edge("edit_code", "generate_response")
    workflow.add_edge("generate_text", "generate_response")
    workflow.add_edge("edit_text", "generate_response")
    
    # Add edge from response generator to end
    workflow.add_edge("generate_response", END)
    
    return workflow.compile()


class GraphManager:
    def __init__(self, config):
        self.config = config
        self.graph = None
    
    def __enter__(self):
        self.graph = build_graph()
        return self.graph

    def __exit__(self,exc_type, exc_val, exc_tb):
        logging.info("Cleaning up graph resources")

        return False