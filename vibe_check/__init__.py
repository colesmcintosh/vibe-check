"""
Vibe Check - A professional CLI tool for security analysis using Claude 4
"""

__version__ = "1.0.0"
__author__ = "Cole McIntosh"
__email__ = "colemcintosh6@gmail.com"
__description__ = "A professional CLI tool for security analysis using Claude 4"
__url__ = "https://github.com/colesmcintosh/vibe-check"

from .cli import main

__all__ = ["main", "__version__"] 