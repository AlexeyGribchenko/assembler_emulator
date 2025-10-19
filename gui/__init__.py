"""
GUI of Assembler IDE
"""

__version__ = '1.0.0'

from .gui import AssemblerIDE

DEFAULT_WINDOW_SIZE = "800x600"

__all__ = [
    'AssemblerIDE',
    'DEFAULT_WINDOW_SIZE'
]