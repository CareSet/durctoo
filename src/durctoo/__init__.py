"""
durctoo - HTML5 Form Generator Library
"""

__version__ = '0.1.0'

from .form_data import HTML5FormData, FormMethod, InputType
from .forms import FormGenerator
from .templates import AbstractFormTemplate, Bootstrap5FormTemplate, BulmaFormTemplate, MaterializeFormTemplate

__all__ = [
    'HTML5FormData',
    'FormMethod',
    'InputType',
    'FormGenerator',
    'AbstractFormTemplate',
    'Bootstrap5FormTemplate',
    'BulmaFormTemplate',
    'MaterializeFormTemplate',
]
