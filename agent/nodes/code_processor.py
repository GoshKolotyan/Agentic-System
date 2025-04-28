from ..utils.state import MessageState
from ..utils.llm import query_llm, extract_code_from_markdown
from ..utils.file_utils import FileUtils

def generate_code(state: MessageState) -> MessageState:
    """generate code based on user request. """
    user_message = state["messages"][-1].content
    language = state.get("language") or "python"
    
    prompt = f"""
    Generate code based on the following request:
    {user_message}
    
    Programming language: {language}
    
    Provide only the code with appropriate comments but no additional explanations.
    """
    
    code_with_markdown = query_llm(prompt)
    
    code = extract_code_from_markdown(code_with_markdown, language)
    
    output_file = FileUtils.get_output_filename(language, is_code=True)
    
    success = FileUtils.write_to_file(output_file, code)
    
    response = f"Generated {language} code and saved to {output_file}"
    if not success:
        response = f"Error saving {language} code to {output_file}"
    
    return {
        **state,
        "source_code": code,
        "output_file": output_file,
        "response": response
    }

def edit_code(state: MessageState) -> MessageState:
    """Edit existing code based on user request."""
    user_message = state["messages"][-1].content
    language = state.get("language") or "python"
    
    file_to_edit = FileUtils.get_existing_file_for_language(language)
    
    existing_code = FileUtils.read_file_if_exists(file_to_edit)
    
    prompt = f"""
    Edit the following code based on the user's request:
    
    User request: {user_message}
    
    Existing code:
    ```{language}
    {existing_code}
    ```
    
    Provide the complete edited code with no additional explanations.
    """

    edited_code_with_markdown = query_llm(prompt)
    
    edited_code = extract_code_from_markdown(edited_code_with_markdown, language)
    
    success = FileUtils.write_to_file(file_to_edit, edited_code)
    
    response = f"Edited {language} code and saved to {file_to_edit}"
    if not success:
        response = f"Error saving edited {language} code to {file_to_edit}"
    
    return {
        **state,
        "source_code": edited_code,
        "output_file": file_to_edit,
        "response": response
    }