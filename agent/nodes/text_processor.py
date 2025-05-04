import logging
from ..utils.state import MessageState
from ..utils.llm import query_llm, extract_code_from_markdown
from ..utils.file_utils import FileUtils

def generate_text(state: MessageState) -> MessageState:
    """ Generate free text based on user request"""
    user_message = state["messages"][-1].content
    filename = state.get("filename") or "output.txt"
    prompt = f"""
    Generate text based on the following request:
    {user_message}
    
    Provide the text with no additional explanations or markdown formatting.
    """
    generated_text = query_llm(prompt)
    
    if "```" in generated_text:
        generated_text = extract_code_from_markdown(generated_text)
    
    output_file = FileUtils.get_textgen_filename(filename=filename)
    
    success = FileUtils.write_to_file(output_file, generated_text, is_code=False, is_question=False, is_text=True)
    
    # logging.info(f"Generated text: {generated_text}")
    response = f"Generated text and saved to {output_file}"
    if not success:
        response = f"Error saving generated text to {output_file}"
    
    return {
        **state,
        "source_text": generated_text,
        "output_file": output_file,
        "response": response
    }

def edit_text(state: MessageState) -> MessageState:
    """edit existing text based on user request."""
    user_message = state["messages"][-1].content
    filename = state.get("filename") or "output.txt"
    
    output_file = FileUtils.get_textgen_filename(filename=filename)
    
    existing_text = FileUtils.get_existing_file_for_language(output_file)
    
    prompt = f"""
    Edit the following text based on the user's request:
    
    User request: {user_message}
    
    
    Provide the complete edited text with no additional explanations or markdown formatting.
    """
    
    edited_text_with_markdown = query_llm(prompt)
    
    if "```" in edited_text_with_markdown:
        edited_text = extract_code_from_markdown(edited_text_with_markdown)
    else:
        edited_text = edited_text_with_markdown
    
    success = FileUtils.write_to_file(existing_text, edited_text, is_code=False, is_question=False, is_text=True)

    # logging.info(f"Edited text: {edited_text}")
    response = f"Edited text and saved to {existing_text}"
    if not success:
        response = f"Error saving edited text to {existing_text}"
    
    return {
        **state,
        "source_text": edited_text,
        "output_file": output_file,
        "response": response
    }