import os
import logging
from ..config import Config

class FileUtils:
    def __init__(self):
        self.config = Config()
    @staticmethod
    def get_output_filename(self, language: str = None, is_code: bool = True) -> str:
        """get output filename for code or text"""
        if is_code and language:
            extension = self.config.FILE_EXTENSIONS.get(language.lower(), ".txt")
            return f"output{extension}"
        elif is_code:
            return self.config.DEFAULT_CODE_OUTPUT
        else:
            return self.config.DEFAULT_TEXT_OUTPUT

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
    def get_existing_file_for_language(self, language: str) -> str:
        """get existing file for language"""
        extension = self.config.FILE_EXTENSIONS.get(language.lower(), ".txt")
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