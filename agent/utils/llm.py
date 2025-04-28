
import json
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from ..config import Config

def query_llm(prompt: str, parse_json: bool = False):
    """
    query the llm with a prompt
    """
    config = Config()
    llm = ChatOpenAI(model=config.DEFAULT_MODEL, temperature=config.TEMPERATURE) # can be change into claude 3.5 sonnet or other models
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content
    
    if parse_json:
        try:
            #make sure the content is json
            if "```json" in content and "```" in content:
                #removing json part
                content = content.split("```json")[1].split("```")[0].strip()
                logging.info(f"Parsed content as JSON is :{content}")
            elif "```" in content and content.count("```") >= 2:
                #content from any code block
                content = content.split("```")[1].split("```")[0].strip()
                logging.info(f"Parsed content from code block is :{content}")
            return json.loads(content)
        except json.JSONDecodeError:
            #if JSON parsing fails
            try:
                # finding similar json structure
                if "{" in content and "}" in content:
                    json_str = content.split("{", 1)[1].rsplit("}", 1)[0].strip()
                    json_str = "{" + json_str + "}"
                    return json.loads(json_str)
            except (IndexError, json.JSONDecodeError):
                # return raw content is json parsing fails
                logging.warning("Warning: Failed to parse JSON from LLM response")
                return {"error": "Failed to parse JSON", "raw_content": content}
    
    return content

def extract_code_from_markdown(code_text: str, language: str = None) -> str:
    """
    clean code from markdown
    """
    if "```" in code_text:
        parts = code_text.split("```")
        
        if len(parts) >= 3:
            code = parts[1]
            
            if language and code.startswith(language):
                code = code[len(language):].strip()
            elif code.split("\n", 1)[0].strip() and not code.split("\n", 1)[0].strip().startswith("```"):
                code = code.split("\n", 1)[1].strip()
                
            return code

    logging.warning("Warning: No code block found in the text")
    return code_text