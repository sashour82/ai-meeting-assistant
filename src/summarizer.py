"""
Meeting summarization module using OpenAI GPT models.
"""

import logging
from typing import Optional

import openai
from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


class MeetingSummarizer:
    """Handles meeting text summarization using OpenAI GPT models."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the Meeting Summarizer.
        
        Args:
            api_key: OpenAI API key. If None, uses environment variable.
            model: GPT model to use. If None, uses default from settings.
        """
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.GPT_MODEL
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. "
                "Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        openai.api_key = self.api_key
        logger.info(f"Meeting Summarizer initialized with model: {self.model}")
    
    def summarize(self, meeting_text: str) -> str:
        """
        Summarize meeting transcript in Arabic.
        
        Args:
            meeting_text: The transcribed meeting text
            
        Returns:
            Formatted summary of the meeting
            
        Raises:
            ValueError: If meeting_text is empty
            Exception: If summarization fails
        """
        if not meeting_text or not meeting_text.strip():
            raise ValueError("Meeting text cannot be empty")
        
        try:
            logger.info(f"Starting summarization. Text length: {len(meeting_text)} characters")
            
            prompt = settings.SUMMARY_PROMPT_TEMPLATE.format(meeting_text=meeting_text)
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "أنت مساعد ذكي متخصص في تلخيص الاجتماعات باللغة العربية."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent summaries
                max_tokens=1000   # Limit response length
            )
            
            summary = response.choices[0].message.content
            logger.info("Summarization completed successfully")
            
            return summary
            
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            raise Exception(f"Summarization failed: {str(e)}")


# Backward compatibility function
def summarize_meeting(meeting_text: str) -> str:
    """
    Legacy function for backward compatibility.
    
    Args:
        meeting_text: The meeting text to summarize
        
    Returns:
        Meeting summary
    """
    summarizer = MeetingSummarizer()
    return summarizer.summarize(meeting_text)
