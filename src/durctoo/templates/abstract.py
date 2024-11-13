# src/durctoo/templates/abstract.py

from abc import ABC, abstractmethod
from typing import Tuple
from ..form_data import HTML5FormData

class AbstractFormTemplate(ABC):
    """Abstract base class for form templates that generate HTML5 forms.
    
    This class defines the interface that all form template implementations must follow.
    The only method that must be implemented by child classes is buildHTML, as it's
    possible to have form templates that don't require additional CSS or JavaScript.
    """
    
    @classmethod
    def buildForm(cls, form_data: HTML5FormData) -> Tuple[str, str, str]:
        """Build complete form including CSS, HTML, and JavaScript.
        
        Args:
            form_data: HTML5FormData object containing form definition
            
        Returns:
            Tuple of (CSS, HTML, JavaScript) strings
        """
        css = cls.buildCSS(form_data)
        js = cls.buildJS(form_data)
        html = cls.buildHTML(form_data)
        return (css, html, js)
    
    @classmethod
    def buildCSS(cls, form_data: HTML5FormData) -> str:
        """Build CSS for form. Default implementation returns empty string.
        
        Args:
            form_data: HTML5FormData object containing form definition
            
        Returns:
            CSS string
        """
        return ""
    
    @classmethod
    def buildJS(cls, form_data: HTML5FormData) -> str:
        """Build JavaScript for form. Default implementation returns empty string.
        
        Args:
            form_data: HTML5FormData object containing form definition
            
        Returns:
            JavaScript string
        """
        return ""
    
    @classmethod
    @abstractmethod
    def buildHTML(cls, form_data: HTML5FormData) -> str:
        """Build HTML for form. Must be implemented by child classes.
        
        Args:
            form_data: HTML5FormData object containing form definition
            
        Returns:
            HTML string
        """
        pass
