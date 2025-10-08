"""
Gradio web interface for the AI Meeting Assistant.
"""

import logging
from typing import Tuple, Optional

import gradio as gr
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.speech_to_text import SpeechToTextProcessor
from src.summarizer import MeetingSummarizer
from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


class MeetingAssistantInterface:
    """Gradio interface for the AI Meeting Assistant."""
    
    def __init__(self):
        """Initialize the interface components."""
        self.stt_processor = SpeechToTextProcessor()
        self.summarizer = MeetingSummarizer()
        self._setup_langchain_chain()
    
    def _setup_langchain_chain(self):
        """Set up the LangChain processing chain."""
        try:
            prompt = ChatPromptTemplate.from_template(settings.LANGCHAIN_PROMPT_TEMPLATE)
            
            self.chain = (
                {"meeting_text": RunnablePassthrough()}
                | prompt
                | StrOutputParser()
            )
            
            logger.info("LangChain processing chain initialized successfully")
            
        except Exception as e:
            logger.warning(f"Failed to initialize LangChain chain: {e}")
            self.chain = None
    
    def process_meeting(self, audio_file: Optional[str]) -> Tuple[str, str]:
        """
        Process an audio file: transcribe and summarize.
        
        Args:
            audio_file: Path to the audio file
            
        Returns:
            Tuple of (transcribed_text, summary)
        """
        if not audio_file:
            return "⚠️ الرجاء رفع ملف صوتي أولاً.", ""
        
        try:
            logger.info(f"Processing audio file: {audio_file}")
            
            # Step 1: Speech-to-Text
            meeting_text = self.stt_processor.transcribe(audio_file)
            
            # Step 2: Summarization using LangChain if available, otherwise direct summarization
            if self.chain:
                summary = self.chain.invoke({"meeting_text": meeting_text})
            else:
                summary = self.summarizer.summarize(meeting_text)
            
            logger.info("Meeting processing completed successfully")
            return meeting_text, summary
            
        except Exception as e:
            error_msg = f"حدث خطأ أثناء المعالجة: {e}"
            logger.error(f"Error in process_meeting: {e}")
            return error_msg, ""
    
    def create_interface(self) -> gr.Blocks:
        """
        Create and configure the Gradio interface.
        
        Returns:
            Configured Gradio interface
        """
        css = """
        body {direction: rtl; text-align: right;} 
        * {font-family: 'Cairo', sans-serif;}
        """
        
        with gr.Blocks(css=css) as demo:
            gr.Markdown(
                "## 🤖 مساعد الاجتماعات الذكي (نسخة متقدمة)\n"
                "### رفع الصوت → تحويل النص → تلخيص الاجتماع"
            )
            
            with gr.Row():
                with gr.Column():
                    audio_input = gr.Audio(
                        label="🎧 ارفع تسجيل الاجتماع (MP3 أو WAV)", 
                        type="filepath"
                    )
                    process_btn = gr.Button("🚀 تحليل الاجتماع", variant="primary")
                
                with gr.Column():
                    transcribed_text = gr.Textbox(
                        label="📝 النص المستخرج من التسجيل", 
                        lines=10, 
                        interactive=False
                    )
                    summarized_text = gr.Textbox(
                        label="📄 ملخص الاجتماع", 
                        lines=10, 
                        interactive=False
                    )
            
            process_btn.click(
                self.process_meeting,
                inputs=[audio_input],
                outputs=[transcribed_text, summarized_text]
            )
        
        return demo
    
    def launch(self, **kwargs):
        """
        Launch the Gradio interface.
        
        Args:
            **kwargs: Additional arguments for demo.launch()
        """
        demo = self.create_interface()
        
        # Default launch parameters
        launch_params = {
            "server_name": "127.0.0.1",
            "server_port": 7860,
            "share": False
        }
        launch_params.update(kwargs)
        
        logger.info(f"Launching interface with parameters: {launch_params}")
        demo.launch(**launch_params)


def main():
    """Main function to run the AI Meeting Assistant."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        interface = MeetingAssistantInterface()
        interface.launch()
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise


if __name__ == "__main__":
    main()
