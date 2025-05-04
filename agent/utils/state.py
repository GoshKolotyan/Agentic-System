from typing import Optional, Union, TypedDict, List, Tuple
import re
from langchain_core.messages import HumanMessage, AIMessage

class MessageState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]  # messages of the conversation
    intent: Optional[str]  # intent of the user
    language: Optional[str]  # language of the code
    source_code: Optional[str]  # source code of the code
    source_text: Optional[str]  # source text of the text
    output_file: Optional[str]  # output file of the code
    response: Optional[str]  # response of the code

#TODO add short term and long term memory here 

def detect_language_from_message(message: str) -> Optional[str]:
    """
    Detects programming language from a message by looking for common patterns:
    1. Explicit mentions like "in Python" or "using JavaScript"
    2. Code blocks with language specifiers like ```python or ```js
    3. Common file extensions like .py, .js, etc.
    """
    # Check for explicit language mentions
    language_patterns = {
        r'\b(?:in|using|with)\s+python\b': 'python',
        r'\b(?:in|using|with)\s+javascript\b': 'javascript',
        r'\b(?:in|using|with)\s+js\b': 'javascript',
        r'\b(?:in|using|with)\s+java\b': 'java',
        r'\b(?:in|using|with)\s+c\+\+\b': 'cpp',
        r'\b(?:in|using|with)\s+c#\b': 'csharp',
        r'\b(?:in|using|with)\s+go\b': 'go',
        r'\b(?:in|using|with)\s+rust\b': 'rust',
        r'\b(?:in|using|with)\s+typescript\b': 'typescript',
        r'\b(?:in|using|with)\s+ruby\b': 'ruby',
        r'\b(?:in|using|with)\s+php\b': 'php',
        r'\b(?:in|using|with)\s+swift\b': 'swift',
        r'\b(?:in|using|with)\s+kotlin\b': 'kotlin',
        r'\b(?:in|using|with)\s+scala\b': 'scala',
    }
    
    for pattern, lang in language_patterns.items():
        if re.search(pattern, message, re.IGNORECASE):
            return lang
    
    code_block_pattern = r'```([a-zA-Z0-9_+#]+)[\s\n]'
    code_blocks = re.findall(code_block_pattern, message)
    if code_blocks:
        lang = code_blocks[0].lower()
        # Map some common abbreviations
        lang_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'rb': 'ruby',
            'cs': 'csharp',
        }
        return lang_map.get(lang, lang)
    
    # Check for file extensions
    file_ext_pattern = r'\b\w+\.(py|js|java|cpp|cs|go|rs|ts|rb|php|swift|kt|scala)\b'
    file_exts = re.findall(file_ext_pattern, message)
    if file_exts:
        ext = file_exts[0].lower()
        ext_map = {
            'py': 'python',
            'js': 'javascript',
            'java': 'java',
            'cpp': 'cpp',
            'cs': 'csharp',
            'go': 'go',
            'rs': 'rust',
            'ts': 'typescript',
            'rb': 'ruby',
            'php': 'php',
            'swift': 'swift',
            'kt': 'kotlin',
            'scala': 'scala',
        }
        return ext_map.get(ext)
    
    return None

def extract_output_file(message: str) -> Optional[str]:
    """
    Extracts potential output file paths from a message.
    Looks for patterns like "save to X", "output to X", "write to X", etc.
    """
    # Patterns that might indicate output files
    output_patterns = [
        r'(?:save|output|write|export|store)(?:\s+(?:it|this|the\s+(?:result|code|output)))?\s+(?:to|in|as|in\s+file|to\s+file|as\s+file)\s+[\'"]?([a-zA-Z0-9_\-\.\/\\]+\.[a-zA-Z0-9]+)[\'"]?',
        r'output\s+file\s*(?:is|should\s+be|:)?\s+[\'"]?([a-zA-Z0-9_\-\.\/\\]+\.[a-zA-Z0-9]+)[\'"]?',
        r'filename\s*(?:is|should\s+be|:)?\s+[\'"]?([a-zA-Z0-9_\-\.\/\\]+\.[a-zA-Z0-9]+)[\'"]?'
    ]
    
    for pattern in output_patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

def parse_user_message(message: str) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Parses a user message to extract language, source code, source text, and output file.
    """
    language = detect_language_from_message(message)
    output_file = extract_output_file(message)
    
    return language, output_file

def create_initial_state(user_input: str) -> MessageState:
    """
    Creates the initial state with auto-detected language, source code, source text, 
    and output file if possible
    """
    language, output_file = parse_user_message(user_input)
    
    return {
        "messages": [HumanMessage(content=user_input)],
        "intent": None,
        "language": language,
        "output_file": output_file,
        "response": None
    }