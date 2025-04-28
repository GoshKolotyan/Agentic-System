import os
import logging
from ..config import Config

class FileUtils:
    def __init__(self):
        self.config = Config()
    
    @staticmethod
    def get_output_filename(language: str = None, filename: str = None, is_code: bool = True) -> str:
        """Determine the appropriate output filename based on provided parameters."""
        config = Config()

        # Case 1: Explicit filename provided (highest priority)
        if filename:
            _, ext = os.path.splitext(filename)
            if ext and is_code:
                logging.info(f"Using explicit filename: {filename}")
                return os.path.join(config.SAVING_FOLDER_CODE, filename)
            elif is_code:
                logging.info(f"Inferred language: {language} and extension: {ext}")
                if language:
                    ext = config.FILE_EXTENSIONS.get(language.lower(), ".txt")
                    new_filename = f"{filename}{ext}"
                    logging.info(f"Adding extension to filename: {new_filename}")
                    return os.path.join(config.SAVING_FOLDER_CODE, new_filename)
                else:
                    logging.info(f"Using filename without known extension: {filename}")
                    return os.path.join(config.SAVING_FOLDER_CODE, filename)
            else:
                logging.info(f"Saving text with filename: {filename}")
                return os.path.join(config.SAVING_FOLDER_TEXT, filename)
            
        # Case 2: No filename but language specified (for code)
        if is_code and language:
            ext = config.FILE_EXTENSIONS.get(language.lower())
            if not ext:
                logging.warning(f"No extension found for language: {language}. Using .txt as default.")
                ext = ".txt"
            
            output_name = f"output{ext}"
            logging.info(f"Generated filename based on language: {output_name}")
            return os.path.join(config.SAVING_FOLDER_CODE, output_name)
        
        # Case 3: Code but no language specified
        elif is_code:
            output_name = config.DEFAULT_CODE_OUTPUT
            logging.info(f"Using default code output: {output_name}")
            return os.path.join(config.SAVING_FOLDER_CODE, output_name)
        
        # Case 4: Not code (text content)
        else:
            output_name = config.DEFAULT_TEXT_OUTPUT
            logging.info(f"Using default text output: {output_name}")
            return os.path.join(config.SAVING_FOLDER_TEXT, output_name)
    
    @staticmethod
    def read_file_if_exists(filename: str) -> str:
        """read file if it exists"""
        if os.path.exists(filename):
            try:
                logging.info(f"Reading file: {filename}")
                with open(filename, "r") as f:
                    return f.read()
            except Exception as e:
                logging.error(f"Error reading file: {str(e)}")
                return f"Error reading file: {str(e)}"
        else:
            return f"# File {filename} does not exist. Creating new file."
    
    @staticmethod
    def write_to_file(filename: str, content: str) -> bool:
        """write content to a file."""
        try:
            logging.info(f"Writing to file: {filename}")
            with open(filename, "w") as f:
                f.write(content)
            return True
        except Exception as e:
            logging.error(f"Error writing to {filename}: {str(e)}")
            return False
    
    @staticmethod
    def get_existing_file_for_language(language: str) -> str:
        """get existing file for language"""
        config = Config()  
        
        extension = config.FILE_EXTENSIONS.get(language.lower(), ".txt")
        default_filename = f"output{extension}"
        
        if os.path.exists(default_filename):
            logging.info(f"Existing file found: {default_filename}")
            return default_filename
            
        for filename in os.listdir("."):
            if filename.endswith(extension):
                logging.info(f"Found existing file: {filename}")
                return filename
                
        logging.info(f"No existing file found, returning default: {default_filename}")
        return default_filename