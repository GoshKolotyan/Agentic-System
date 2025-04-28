class TaskRouter:
    """
    Routes tasks to appropriate handlers based on intent analysis.
    """
    def __init__(self):
        # This will hold references to our handler functions
        self.handlers = {
            "question": self._handle_question,
            "code_gen": self._handle_code_generation,
            "code_edit": self._handle_code_editing,
            "text_gen": self._handle_text_generation,
            "text_edit": self._handle_text_editing
        }
    
    def route(self, intent_analysis, user_message):
        """
        Route the task to the appropriate handler.
        
        Args:
            intent_analysis: The IntentAnalysis object from the analyzer
            user_message: The original user message
            
        Returns:
            The result from the handler
        """
        # Get the appropriate handler based on intent type
        handler = self.handlers.get(
            intent_analysis.intent_type, 
            self._handle_unknown
        )
        
        # Call the handler with the intent details and original message
        return handler(intent_analysis.details, user_message)
    
    def _handle_question(self, details, message):
        """Placeholder for question handler."""
        return {
            "status": "success",
            "response_type": "answer",
            "content": f"This would answer the question: {message}",
            "details": details
        }
    
    def _handle_code_generation(self, details, message):
        """Placeholder for code generation handler."""
        language = details.get("language", "unknown")
        return {
            "status": "success",
            "response_type": "code_gen",
            "content": f"This would generate {language} code for: {message}",
            "details": details
        }
    
    def _handle_code_editing(self, details, message):
        """Placeholder for code editing handler."""
        files = details.get("files", [])
        file_names = [f["filename"] for f in files] if files else ["unknown file"]
        return {
            "status": "success",
            "response_type": "code_edit",
            "content": f"This would edit {', '.join(file_names)} as requested",
            "details": details
        }
    
    def _handle_text_generation(self, details, message):
        """Placeholder for text generation handler."""
        content_type = details.get("content_type", "content")
        return {
            "status": "success",
            "response_type": "text_gen",
            "content": f"This would generate {content_type} about: {message}",
            "details": details
        }
    
    def _handle_text_editing(self, details, message):
        """Placeholder for text editing handler."""
        return {
            "status": "success",
            "response_type": "text_edit",
            "content": f"This would edit text content as requested",
            "details": details
        }
    
    def _handle_unknown(self, details, message):
        """Handler for unknown intent types."""
        return {
            "status": "error",
            "response_type": "unknown",
            "content": f"I'm not sure how to process this request: {message}",
            "details": details
        }