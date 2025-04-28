# main.py
import logging
from src.input_handler import get_user_input
from src.intent_analyzer import IntentAnalyzer
from src.task_router import TaskRouter

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Main program loop."""
    logging.info("Welcome to the Agentic Program!")
    logging.info("Type your messages below. Press Ctrl+C to exit.")
    
    # Initialize components
    analyzer = IntentAnalyzer()
    router = TaskRouter()
    
    try:
        while True:
            # Step 1: Get user input
            user_message = get_user_input()
            
            # Step 2: Analyze intent
            intent_analysis = analyzer.analyze(user_message)
            
            # Log the intent analysis
            logging.info("\nIntent Analysis:")
            logging.info(f"- Intent Type: {intent_analysis.intent_type}")
            logging.info(f"- Confidence: {intent_analysis.confidence:.2f}")
            logging.info("- Details:")
            for key, value in intent_analysis.details.items():
                logging.info(f"  - {key}: {value}")
            
            # Step 3: Route to appropriate handler
            result = router.route(intent_analysis, user_message)
            
            # Step 4: Display the result
            logging.info("\nTask Result:")
            logging.info(f"- Response Type: {result['response_type']}")
            logging.info(f"- Content: {result['content']}")
            
            # For demonstration, also log the original message
            logging.info(f"Received: {user_message}")
            
    except KeyboardInterrupt:
        logging.info("\nExiting program. Goodbye!")

if __name__ == "__main__":
    main()