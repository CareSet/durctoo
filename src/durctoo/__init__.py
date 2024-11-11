"""
Durctoo - HTML5 Form Data Modeling Package

A Python package that provides clean abstractions for modeling HTML5 form data,
independent of any specific web framework or rendering engine.
"""

from .forms import HTML5FormData, FormMethod, InputType
from .version import __version__

__all__ = ['HTML5FormData', 'FormMethod', 'InputType', '__version__']
