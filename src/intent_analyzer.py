# src/intent_analyzer.py (enhanced)
import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Dict, Optional, List

# Load environment variables from .env file
load_dotenv()

class IntentAnalysis(BaseModel):
    """
    Structured output for intent analysis.
    """
    intent_type: str = Field(
        description="Type of intent: question, code_gen, code_edit, text_gen, or text_edit"
    )
    confidence: float = Field(
        description="Confidence level in the classification (0.0-1.0)"
    )
    details: Dict = Field(
        description="Additional details extracted from the request",
        default={}
    )

class IntentAnalyzer:
    """
    Analyzes user messages to determine intent and extract metadata.
    """
    def __init__(self, model_name="gpt-3.5-turbo"):
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model=model_name, 
            temperature=0.0,  # We want deterministic classification
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Set up the output parser
        self.parser = PydanticOutputParser(pydantic_object=IntentAnalysis)
        
        # File extensions to programming languages mapping
        self.file_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.html': 'html',
            '.css': 'css',
            '.java': 'java',
            '.cpp': 'c++',
            '.c': 'c',
            '.rb': 'ruby',
            '.php': 'php',
            '.go': 'go',
            '.rs': 'rust',
            '.ts': 'typescript',
            '.sh': 'bash',
            '.md': 'markdown',
            '.txt': 'text',
        }
        
        # Create the prompt template
        template = """
        You are an expert intent classifier. Analyze the following user message and determine what they want.
        
        Possible intents:
        1. question - User is asking a question and wants a direct answer
        2. code_gen - User wants to generate new code
        3. code_edit - User wants to edit existing code
        4. text_gen - User wants to generate new text content
        5. text_edit - User wants to edit existing text content
        
        User message: {message}
        
        For code-related intents, extract details like:
        - Programming language requested
        - Task description
        - Filename if mentioned
        
        For text-related intents, extract details like:
        - Content type (blog post, email, etc.)
        - Topic or subject
        - Style requirements
        - Filename if mentioned
        
        {format_instructions}
        """
        
        self.prompt = ChatPromptTemplate.from_template(
            template=template,
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        # Create the classification chain
        self.chain = self.prompt | self.llm | self.parser
    
    def _extract_file_references(self, message):
        """
        Extract potential file references from the message.
        """
        # Look for words that might be filenames with extensions
        potential_files = re.findall(r'\b[\w\-\.]+\.[a-zA-Z]{1,5}\b', message)
        
        files = []
        for file in potential_files:
            _, ext = os.path.splitext(file)
            if ext in self.file_extensions:
                language = self.file_extensions[ext]
                files.append({
                    'filename': file,
                    'extension': ext,
                    'language': language,
                    'exists': os.path.exists(file)
                })
        
        return files
    
    def analyze(self, user_message):
        """
        Analyze the user message to determine intent and extract metadata.
        
        Args:
            user_message: The message from the user
            
        Returns:
            IntentAnalysis object with classification and metadata
        """
        try:
            # First extract file references
            files = self._extract_file_references(user_message)
            
            # Run the classification chain
            result = self.chain.invoke({"message": user_message})
            
            # Add file information to the details if not already present
            if files and 'files' not in result.details:
                result.details['files'] = files
                
                # If we detected files and it's an edit request, make sure we have the right intent
                if any(f['exists'] for f in files) and 'edit' in user_message.lower():
                    # Determine if it's likely code or text
                    code_files = [f for f in files if f['extension'] not in ['.txt', '.md']]
                    if code_files:
                        result.intent_type = 'code_edit'
                    else:
                        result.intent_type = 'text_edit'
            
            return result
        except Exception as e:
            print(f"Error analyzing intent: {e}")
            # Return a fallback intent analysis
            return IntentAnalysis(
                intent_type="question",  # Default to treating it as a question
                confidence=0.3,
                details={"error": str(e)}
            )