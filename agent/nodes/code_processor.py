from typing import TypedDict
from ..utils.state import MessageState
from ..utils.llm import query_llm, extract_code_from_markdown
from ..utils.file_utils import FileUtils

class CodeProcessor:
    def __init__(self, state: dict):
        self.state = state
        self.user_message = state['messages'][-1].content
        self.language = state.get('language') or 'python'
    
    def process(self) -> dict:
        prompt = self._build_prompt()
        
        # LLM and extract code
        code_with_markdown = self._query_llm(prompt)
        processed_code = self._extract_code(code_with_markdown)
        
        #for saving
        output_file = self._get_output_file()
        success = self._save_to_file(output_file, processed_code)
        
        #build respone message
        response = self._build_response(success, output_file)
        
        
        return {
            **self.state,
            "source_code": processed_code,
            "output_file": output_file,
            "response": response
        }
    
    def _query_llm(self, prompt: str) -> str:
        return query_llm(prompt)
    
    def _extract_code(self, code_with_markdown: str) -> str:
        return extract_code_from_markdown(code_with_markdown, self.language)
    
    def _save_to_file(self, file_path: str, code: str) -> bool:
        return FileUtils.write_to_file(
            filename=file_path,
            content=code,
            is_code=True
        )
    
    def _build_prompt(self) -> str:
        raise NotImplementedError
    
    def _get_output_file(self) -> str:
        raise NotImplementedError
    
    def _build_response(self, success: bool, output_file: str) -> str:
        raise NotImplementedError
    
class CodeGenerator(CodeProcessor):
    """Class for generating code."""

    def _build_prompt(self) -> str:
        return f"""
        Generate code based on the following request:
        {self.user_message}
        
        Programming language: {self.language}
        
        Provide only the code with appropriate comments but no additional explanations.
        """
    def _get_output_file(self) -> str:
        filename = self.state.get("output_file") or "output.py"
        return FileUtils.get_code_filename(filename=filename)
    
    def _build_response(self, success: bool, output_file: str) -> str:
        if success:
            return f"Generated {self.language} code and saved to {output_file}"
        else:
            return f"Error saving {self.language} code to {output_file}"
    
class CodeEditor(CodeProcessor):
    """Class for editing existing code."""
    
    def __init__(self, state: dict):
        super().__init__(state)
        self.file_to_edit = FileUtils.get_existing_file_for_language(self.language)
        self.existing_code = FileUtils.read_file_if_exists(self.file_to_edit)
    
    def _build_prompt(self) -> str:
        return f"""
        Edit the following code based on the user's request:
        
        User request: {self.user_message}
        
        Existing code:
        ```{self.language}
        {self.existing_code}
        ```
        
        Provide the complete edited code with no additional explanations.
        """
    
    def _get_output_file(self) -> str:
        return self.file_to_edit
    
    def _build_response(self, success: bool, output_file: str) -> str:
        if success:
            return f"Edited {self.language} code and saved to {output_file}"
        else:
            return f"Error saving edited {self.language} code to {output_file}"


def generate_code(state: dict) -> dict:
    """Generate code based on user request."""
    generator = CodeGenerator(state)
    return generator.process()

def edit_code(state: dict) -> dict:
    """Edit existing code based on user request."""
    editor = CodeEditor(state)
    return editor.process()