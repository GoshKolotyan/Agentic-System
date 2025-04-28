import os
import logging

class Config:
    # llm configs
    DEFAULT_MODEL = "gpt-3.5-turbo" # default model can be chnaged into gpt-4 or other models
    TEMPERATURE = 0 # 0 is deterministic for this case I prefer deterministic
    
    # File Extensions by Language
    FILE_EXTENSIONS = {
        "python": ".py", 
        "javascript": ".js", 
        "typescript": ".ts", 
        "java": ".java",
        "cpp": ".cpp", 
        "c++": ".cpp", 
        "c": ".c", 
        "go": ".go",
        "rust": ".rs",
        "ruby": ".rb",
        "php": ".php",
        "csharp": ".cs",
        "c#": ".cs",
        "swift": ".swift",
        "kotlin": ".kt",
        "scala": ".scala",
        "shell": ".sh",
        "bash": ".sh",
        "html": ".html",
        "css": ".css"
    }
    
    DEFAULT_CODE_OUTPUT = "output.py"
    DEFAULT_TEXT_OUTPUT = "output.txt"
    
    @staticmethod
    def check_api_key():
        """Check if the OpenAI API key is set."""
        if "OPENAI_API_KEY" not in os.environ:
            logging.warning("OPENAI_API_KEY environment variable is not set.")
            logging.warning("Please see README.md for instructions")
            return False
        logging.info("OPENAI_API_KEY environment variable is set")
        return True