"""
Speech-to-Text processing module using OpenAI Whisper.
"""

import os
import sys
import logging
from typing import Optional
from pathlib import Path

import openai
from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


class SpeechToTextProcessor:
    """Handles audio transcription using OpenAI Whisper API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Speech-to-Text processor.
        
        Args:
            api_key: OpenAI API key. If None, uses environment variable.
        """
        self.api_key = api_key or settings.OPENAI_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not provided. "
                "Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        openai.api_key = self.api_key
        logger.info("Speech-to-Text processor initialized successfully")
    
    def validate_audio_file(self, file_path: str) -> bool:
        """
        Validate that the audio file has a supported format.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            True if file format is supported, False otherwise
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False
        
        if not file_path.suffix.lower() in settings.SUPPORTED_AUDIO_FORMATS:
            logger.error(
                f"Unsupported file format: {file_path.suffix}. "
                f"Supported formats: {settings.SUPPORTED_AUDIO_FORMATS}"
            )
            return False
        
        return True
    
    def transcribe(self, audio_file_path: str) -> str:
        """
        Convert audio file to text using OpenAI Whisper.
        
        Args:
            audio_file_path: Path to the audio file to transcribe
            
        Returns:
            Transcribed text
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file does not exist
            Exception: If transcription fails
        """
        if not self.validate_audio_file(audio_file_path):
            raise ValueError(f"Invalid audio file: {audio_file_path}")
        
        try:
            logger.info(f"Starting transcription of: {audio_file_path}")
            
            with open(audio_file_path, "rb") as audio_file:
                transcript = openai.audio.transcriptions.create(
                    model=settings.WHISPER_MODEL,
                    file=audio_file,
                    language=settings.TRANSCRIPTION_LANGUAGE
                )
            
            transcribed_text = transcript.text
            logger.info(f"Transcription completed successfully. Length: {len(transcribed_text)} characters")
            
            return transcribed_text
            
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            raise Exception(f"Transcription failed: {str(e)}")


# Backward compatibility function
def speech_to_text(audio_file_path: str) -> str:
    """
    Legacy function for backward compatibility.
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        Transcribed text
    """
    processor = SpeechToTextProcessor()
    return processor.transcribe(audio_file_path)
