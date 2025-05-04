import logging
import traceback
from langgraph.graph import StateGraph, END
from typing import Dict, Any, Optional

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

class GraphManager:
    def __init__(self, config):
        self.config = config
        self.graph: Optional[StateGraph] = None
        self.history: list = []

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)


    def __enter__(self):
        try:
            self.graph = self.build_graph()
            # self.logger.info("Graph successfully built and inited")
            return self
        except Exception as e:
            logging.critical(f"Falied to build graph: {str(e)}")
            logging.critical(traceback.format_exc())
            raise

    def __exit__(self,exc_type, exc_val, exc_tb):
        try:
            logging.info("Cleaning up graph resources")
            self.graph = None
            self.history = []
        except Exception as e:
            logging.error(f"Error during graph cleanup: {str(e)}")

        return False    
        
    
    def build_graph(self) -> StateGraph:
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
    
