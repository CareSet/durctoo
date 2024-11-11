# src/durctoo/templates/bootstrap5.py

from typing import Dict, Any
from .abstract import AbstractFormTemplate
from ..forms import HTML5FormData

class Bootstrap5FormTemplate(AbstractFormTemplate):
    """Form template that generates Bootstrap 5.3.3 styled forms."""
    
    @staticmethod
    def buildCSS(form_data: HTML5FormData) -> str:
        """Include Bootstrap 5.3.3 CSS from CDN."""
        return """<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" 
                 rel="stylesheet" 
                 integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" 
                 crossorigin="anonymous">"""
    
    @staticmethod
    def buildJS(form_data: HTML5FormData) -> str:
        """Include Bootstrap 5.3.3 JavaScript from CDN."""
        return """<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" 
                integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" 
                crossorigin="anonymous"></script>"""
    
    @staticmethod
    def buildHTML(form_data: HTML5FormData) -> str:
        """Build Bootstrap 5.3.3 styled HTML form."""
        form_dict = form_data.to_dict()["form"]
        form_header = form_dict["form_header"]
        elements = form_dict["form_element_list"]
        
        # Start form tag with Bootstrap classes
        html = f'<form id="{form_header["form_id"]}" '
        html += f'method="{form_header["method"]}" '
        if form_header["action"]:
            html += f'action="{form_header["action"]}" '
        if form_header["enctype"]:
            html += f'enctype="{form_header["enctype"]}" '
        html += 'class="needs-validation" novalidate>\n'
        
        # Add form elements
        for element in elements:
            html += Bootstrap5FormTemplate._build_element(element)
        
        # Add submit button
        html += """  <div class="mb-3">
    <button type="submit" class="btn btn-primary">Submit</button>
  </div>\n"""
        
        # Close form
        html += "</form>"
        return html
    
    @staticmethod
    def _build_element(element: Dict[str, Any]) -> str:
        """Build HTML for a single form element."""
        element_type = element["type"]
        
        if element_type == "input":
            return Bootstrap5FormTemplate._build_input_element(element)
        elif element_type == "textarea":
            return Bootstrap5FormTemplate._build_textarea_element(element)
        elif element_type == "checkbox_group":
            return Bootstrap5FormTemplate._build_checkbox_group(element)
        elif element_type == "radio_group":
            return Bootstrap5FormTemplate._build_radio_group(element)
        elif element_type == "select":
            return Bootstrap5FormTemplate._build_select_element(element)
        elif element_type == "datalist":
            return Bootstrap5FormTemplate._build_datalist_element(element)
        
        return "<!-- Unsupported element type -->\n"
    
    @staticmethod
    def _build_input_element(element: Dict[str, Any]) -> str:
        """Build HTML for input elements."""
        input_type = element["input_type"]
        required = 'required' if element.get("required", False) else ''
        label = element.get("label", "")
        name = element["name"]
        placeholder = element.get("placeholder", "")
        value = element.get("value", "")
        
        if input_type == "checkbox":
            return f"""  <div class="mb-3 form-check">
    <input type="checkbox" class="form-check-input" id="{name}" name="{name}" {required}>
    <label class="form-check-label" for="{name}">{label}</label>
  </div>\n"""
        
        # For other input types
        html = f'  <div class="mb-3">\n'
        if label:
            html += f'    <label for="{name}" class="form-label">{label}</label>\n'
        
        html += f'    <input type="{input_type}" '
        html += f'class="form-control" '
        html += f'id="{name}" '
        html += f'name="{name}" '
        
        if placeholder:
            html += f'placeholder="{placeholder}" '
        if value:
            html += f'value="{value}" '
        if element.get("min_length"):
            html += f'minlength="{element["min_length"]}" '
        if element.get("max_length"):
            html += f'maxlength="{element["max_length"]}" '
        if element.get("pattern"):
            html += f'pattern="{element["pattern"]}" '
        
        html += f'{required}>\n'
        html += '  </div>\n'
        
        return html
    
    @staticmethod
    def _build_textarea_element(element: Dict[str, Any]) -> str:
        """Build HTML for textarea elements."""
        required = 'required' if element.get("required", False) else ''
        name = element["name"]
        label = element.get("label", "")
        rows = element.get("rows", 3)
        cols = element.get("cols", 40)
        placeholder = element.get("placeholder", "")
        value = element.get("value", "")
        
        html = '  <div class="mb-3">\n'
        if label:
            html += f'    <label for="{name}" class="form-label">{label}</label>\n'
        
        html += f'    <textarea class="form-control" id="{name}" name="{name}" '
        html += f'rows="{rows}" cols="{cols}" {required}'
        if placeholder:
            html += f' placeholder="{placeholder}"'
        html += f'>{value}</textarea>\n'
        html += '  </div>\n'
        
        return html
    
    @staticmethod
    def _build_checkbox_group(element: Dict[str, Any]) -> str:
        """Build HTML for checkbox groups."""
        name = element["name"]
        options = element["options"]
        required = 'required' if element.get("required", False) else ''
        
        html = '  <div class="mb-3">\n'
        for option in options:
            option_value = option["value"]
            option_label = option["label"]
            html += f"""    <div class="form-check">
      <input class="form-check-input" type="checkbox" 
             name="{name}[]" value="{option_value}" 
             id="{name}_{option_value}" {required}>
      <label class="form-check-label" for="{name}_{option_value}">
        {option_label}
      </label>
    </div>\n"""
        html += '  </div>\n'
        
        return html
    
    @staticmethod
    def _build_radio_group(element: Dict[str, Any]) -> str:
        """Build HTML for radio groups."""
        name = element["name"]
        options = element["options"]
        required = 'required' if element.get("required", False) else ''
        default_value = element.get("default_value")
        
        html = '  <div class="mb-3">\n'
        for option in options:
            option_value = option["value"]
            option_label = option["label"]
            checked = 'checked' if option_value == default_value else ''
            html += f"""    <div class="form-check">
      <input class="form-check-input" type="radio" 
             name="{name}" value="{option_value}" 
             id="{name}_{option_value}" {required} {checked}>
      <label class="form-check-label" for="{name}_{option_value}">
        {option_label}
      </label>
    </div>\n"""
        html += '  </div>\n'
        
        return html
    
    @staticmethod
    def _build_select_element(element: Dict[str, Any]) -> str:
        """Build HTML for select elements."""
        name = element["name"]
        options = element["options"]
        required = 'required' if element.get("required", False) else ''
        multiple = 'multiple' if element.get("multiple", False) else ''
        size = element.get("size", "")
        size_attr = f'size="{size}"' if size else ''
        
        html = '  <div class="mb-3">\n'
        html += f'    <select class="form-select" id="{name}" name="{name}" '
        html += f'{required} {multiple} {size_attr}>\n'
        
        for option in options:
            option_value = option["value"]
            option_label = option["label"]
            html += f'      <option value="{option_value}">{option_label}</option>\n'
        
        html += '    </select>\n'
        html += '  </div>\n'
        
        return html
    
    @staticmethod
    def _build_datalist_element(element: Dict[str, Any]) -> str:
        """Build HTML for datalist elements."""
        name = element["name"]
        options = element["options"]
        required = 'required' if element.get("required", False) else ''
        label = element.get("label", "")
        
        html = '  <div class="mb-3">\n'
        if label:
            html += f'    <label for="{name}" class="form-label">{label}</label>\n'
        
        html += f"""    <input class="form-control" list="{name}_list" 
           id="{name}" name="{name}" {required}>\n"""
        html += f'    <datalist id="{name}_list">\n'
        
        for option in options:
            html += f'      <option value="{option}">\n'
        
        html += '    </datalist>\n'
        html += '  </div>\n'
        
        return html
