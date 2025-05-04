import os
import logging
import yaml
class Config:
    configs = yaml.safe_load(open("configs.yaml"))
    # llm configs
    DEFAULT_MODEL = configs["DEFAULT_MODEL"] 
    TEMPERATURE = configs["TEMPERATURE"] 
    
    # File Extensions by Language
    FILE_EXTENSIONS = configs["FILE_EXTENSIONS"]
    
    SAVING_FOLDER = configs["SAVING_FOLDER"]
    SAVING_FOLDER_CODE = configs["SAVING_FOLDER_CODE"]
    SAVING_FOLDER_TEXT = configs["SAVING_FOLDER_TEXT"]
    SAVING_FOLDER_ANSWERS = configs["SAVING_FOLDER_ANSWERS"]
    if not os.path.exists(SAVING_FOLDER_CODE):
        os.makedirs(SAVING_FOLDER_CODE)
    if not os.path.exists(SAVING_FOLDER_TEXT):
        os.makedirs(SAVING_FOLDER_TEXT)
    if not os.path.exists(SAVING_FOLDER_ANSWERS):
        os.makedirs(SAVING_FOLDER_ANSWERS)
    @staticmethod
    def check_api_key():
        """Check if the OpenAI API key is set."""
        if "OPENAI_API_KEY" not in os.environ:
            logging.warning("OPENAI_API_KEY environment variable is not set.")
            logging.warning("Please see README.md for instructions")
            return False
        logging.debug("OPENAI_API_KEY environment variable is set")
        return True