"""
This script performs the following initialization tasks for the application:

1. Configures logging settings, including setting the logging level and adding a console handler.
2. Ensures the presence of a data directory by creating it if it does not already exist.
3. Loads the application state from a predefined source.
4. Initializes a Gradio interface using the loaded state and a specified language (Portuguese).
5. Launches the Gradio interface, which provides a web-based graphical user interface for user interaction.

The Gradio interface allows users to interact with the application through a web-based GUI.
"""

import logging
import os

import gradio as gr

from marketing_sm.business.model import load_state
from marketing_sm.data.constants import DATA_DIR
from marketing_sm.presentation.interface import Interface
from marketing_sm.presentation.language import PortugueseLanguage

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Remove all handlers associated with the root logger object
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

state = load_state()
INTERFACE: Interface = Interface(gr, state, language=PortugueseLanguage())

INTERFACE.launch()
