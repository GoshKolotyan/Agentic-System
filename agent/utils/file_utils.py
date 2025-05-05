import os
import logging
from ..config import Config

class FileUtils:
    def __init__(self):
        self.config = Config()    
    @staticmethod
    def get_code_filename(filename: str = None) -> str:
        """Determine the appropriate output filename based on provided parameters."""
        config = Config()
        if filename:
            return os.path.join(config.SAVING_FOLDER_CODE, filename)
        else:
            return os.path.join(config.SAVING_FOLDER_CODE, f"output")
    @staticmethod
    def get_answer_filename(filename: str = None) -> str:
        """Determine the appropriate output filename based on provided parameters."""
        config = Config()
        if filename:
            return os.path.join(config.SAVING_FOLDER_ANSWERS, filename)
        else:
            return os.path.join(config.SAVING_FOLDER_ANSWERS, "output.txt")
    @staticmethod
    def get_textgen_filename(filename: str = None) -> str:
        """Determine the appropriate output filename based on provided parameters."""
        config = Config()
        if filename:
            return os.path.join(config.SAVING_FOLDER_TEXT, filename)
        else:
            return os.path.join(config.SAVING_FOLDER_TEXT, "output.txt")
    @staticmethod
    def read_file_if_exists(filename: str) -> str:
        """read file if it exists"""
        if os.path.exists(filename):
            try:
                # logging.info(f"Reading file: {filename}")
                with open(filename, "r") as f:
                    return f.read()
            except Exception as e:
                # logging.error(f"Error reading file: {str(e)}")
                return f"Error reading file: {str(e)}"
        else:
            return f"# File {filename} does not exist. Creating new file."
    
    @staticmethod
    def write_to_file(filename: str, content: str, is_question: bool = False, user_message: str = None, is_code: bool = False, is_text: bool = False) -> bool:
        """write content to a file."""
        try:
            # logging.info(f"Writing to file: {filename}")
            with open(filename, "w") as f:
                if is_question:
                    f.write(f"Question: {user_message}\n\n")
                    f.write(f"Answer: {content}\n\n")
                elif is_code:
                    f.write(content)
                elif is_text:
                    f.write(content)
            return True
        except Exception as e:
            # logging.error(f"Error writing to {filename}: {str(e)}")
            return False
    
    @staticmethod
    def get_existing_file_for_language(language: str) -> str:
        """get existing file for language"""
        config = Config()  
        
        extension = config.FILE_EXTENSIONS.get(language.lower(), ".txt")
        if extension == ".txt":
            default_filename = config.SAVING_FOLDER_TEXT + f"/fixed_text{extension}"
        else:
            default_filename = config.SAVING_FOLDER_CODE + f"/fixed_code{extension}"
        
        # if os.path.exists(default_filename):
        #     logging.info(f"Existing file found: {default_filename}")
        #     return default_filename
            
        # for filename in os.listdir("."):
        #     if filename.endswith(extension):
        #         logging.info(f"Found existing file: {filename}")
        #         return filename
                
        # logging.info(f"No existing file found, returning default: {default_filename}")
        return default_filename