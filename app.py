"""
Main entry point for the AI Meeting Assistant application.
"""

import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.interface import MeetingAssistantInterface


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main function to run the AI Meeting Assistant."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting AI Meeting Assistant...")
        interface = MeetingAssistantInterface()
        interface.launch()
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
