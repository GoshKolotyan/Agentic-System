# Logic of class is same for code processing
from ..utils.state import MessageState
from ..utils.llm import query_llm, extract_code_from_markdown
from ..utils.file_utils import FileUtils

class TextProcessor:
    """Base class for processing text requests."""
    
    def __init__(self, state: dict, edit: bool = False):
        self.state = state
        self.user_message = state["messages"][-1].content
        if edit:
            self.filename = state.get("filename") or "fixed_output.txt"
        else:
            self.filename = state.get("filename") or "output.txt"
    
    def process(self) -> dict:
        """Process the text request and return updated state."""
        prompt = self._build_prompt()
        
        generated_text = self._query_llm(prompt)
        
        if "```" in generated_text:
            processed_text = extract_code_from_markdown(generated_text)
        else:
            processed_text = generated_text
        
        output_file = self._get_output_file()
        success = self._save_to_file(output_file, processed_text)
        
        response = self._build_response(success, output_file)
        
        return {
            **self.state,
            "source_text": processed_text,
            "output_file": output_file,
            "response": response
        }
    
    def _query_llm(self, prompt: str) -> str:
        return query_llm(prompt)
    
    def _save_to_file(self, file_path: str, content: str) -> bool:
        return FileUtils.write_to_file(
            file_path, 
            content, 
            is_code=False, 
            is_question=False, 
            is_text=True
        )
    
    def _build_prompt(self) -> str:
        raise NotImplementedError
    
    def _get_output_file(self) -> str:
        raise NotImplementedError
    
    def _build_response(self, success: bool, output_file: str) -> str:
        raise NotImplementedError


class TextGenerator(TextProcessor):
    """Class for generating new text."""
    def __init__(self, state: dict):
        super().__init__(state, edit=False)
        self.filename = state.get("filename") or "output.txt"
    
    def _build_prompt(self) -> str:
        return f"""
        Generate text based on the following request:
        {self.user_message}
        
        Provide the text with no additional explanations or markdown formatting.
        """
    
    def _get_output_file(self) -> str:
        return FileUtils.get_textgen_filename(filename=self.filename)
    
    def _build_response(self, success: bool, output_file: str) -> str:
        if success:
            return f"Generated text and saved to {output_file}"
        else:
            return f"Error saving generated text to {output_file}"
            

class TextEditor(TextProcessor):
    """Class for editing existing text."""
    
    def __init__(self, state: dict):
        super().__init__(state, edit=True)
        self.file_to_edit = FileUtils.get_textgen_filename(filename=self.filename)
        self.existing_text = FileUtils.read_file_if_exists(self.file_to_edit)
    
    def _build_prompt(self) -> str:
        return f"""
        Edit the following text based on the user's request:
        
        User request: {self.user_message}
        
        Existing text:
        {self.existing_text}
        
        Provide the complete edited text with no additional explanations or markdown formatting.
        """
    
    def _get_output_file(self) -> str:
        return self.file_to_edit
    
    def _build_response(self, success: bool, output_file: str) -> str:
        if success: 
            return f"Edited text and saved to {output_file}"
        else:
            return f"Error saving edited text to {output_file}"


def generate_text(state: MessageState) -> MessageState:
    """Generate free text based on user request."""
    generator = TextGenerator(state)
    return generator.process()

def edit_text(state: MessageState) -> MessageState:
    """Edit existing text based on user request."""
    editor = TextEditor(state)
    return editor.process()