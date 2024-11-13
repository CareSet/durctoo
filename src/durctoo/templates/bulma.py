"""
bulma.py - Bulma CSS template for HTML5 forms

This template generates forms styled with the Bulma CSS framework.
https://bulma.io/documentation/form/
"""

from typing import Dict, Any, List, Tuple
from ..forms import HTML5FormData
from .abstract import AbstractFormTemplate

class BulmaFormTemplate(AbstractFormTemplate):
    """Form template that generates HTML5 forms styled with Bulma CSS."""
    
    @classmethod
    def buildCSS(cls, form_data: HTML5FormData) -> str:
        """Include Bulma CSS from CDN."""
        return """
        <style>
            .radio, .checkbox {
                display: block;
                margin-bottom: 0.5rem;
            }
            .file-name {
                max-width: 250px;
            }
            .field:not(:last-child) {
                margin-bottom: 1.5rem;
            }
            .checkbox-group, .radio-group {
                margin-top: 0.5rem;
            }
        </style>
        """

    @classmethod
    def buildJS(cls, form_data: HTML5FormData) -> str:
        """Add minimal JavaScript only for file input UI."""
        return """
        <script>
            document.addEventListener('DOMContentLoaded', () => {
                // File input handling
                const fileInputs = document.querySelectorAll('.file-input');
                fileInputs.forEach(fileInput => {
                    const fileNameSpan = fileInput.parentElement.querySelector('.file-name');
                    fileInput.addEventListener('change', () => {
                        const fileName = fileInput.files[0]?.name || 'No file chosen';
                        fileNameSpan.textContent = fileName;
                    });
                });
            });
        </script>
        """

    @classmethod
    def _render_input(cls, element: Dict[str, Any]) -> str:
        """Render a single input element with Bulma styling."""
        input_type = element.get('input_type', 'text')
        name = element['name']
        required = 'required' if element.get('required', False) else ''
        value = element.get('value', '')
        placeholder = element.get('placeholder', '')
        label = element.get('label', '')
        pattern = f'pattern="{element["pattern"]}"' if element.get('pattern') else ''
        min_length = f'minlength="{element["min_length"]}"' if element.get('min_length') else ''
        max_length = f'maxlength="{element["max_length"]}"' if element.get('max_length') else ''
        
        if input_type == 'checkbox':
            return f"""
            <div class="field">
                <div class="control">
                    <label class="checkbox">
                        <input type="checkbox" name="{name}" {required} {'checked' if element.get('checked') else ''}>
                        {label}
                    </label>
                </div>
            </div>
            """
        
        if input_type == 'file':
            return f"""
            <div class="field">
                <label class="label">{label}</label>
                <div class="control">
                    <div class="file has-name">
                        <label class="file-label">
                            <input class="file-input" type="file" name="{name}" {required}>
                            <span class="file-cta">
                                <span class="file-icon">
                                    <i class="fas fa-upload"></i>
                                </span>
                                <span class="file-label">Choose file...</span>
                            </span>
                            <span class="file-name">No file chosen</span>
                        </label>
                    </div>
                </div>
            </div>
            """
        
        icon = ''
        if input_type == 'email':
            icon = '<span class="icon is-small is-left"><i class="fas fa-envelope"></i></span>'
        elif input_type == 'password':
            icon = '<span class="icon is-small is-left"><i class="fas fa-lock"></i></span>'
        elif input_type == 'tel':
            icon = '<span class="icon is-small is-left"><i class="fas fa-phone"></i></span>'
        elif input_type == 'url':
            icon = '<span class="icon is-small is-left"><i class="fas fa-link"></i></span>'
        elif input_type == 'text':
            icon = '<span class="icon is-small is-left"><i class="fas fa-user"></i></span>'
        
        has_icon = 'has-icons-left' if icon else ''
        
        return f"""
        <div class="field">
            <label class="label">{label}</label>
            <div class="control {has_icon}">
                <input class="input" type="{input_type}" name="{name}"
                       value="{value}" placeholder="{placeholder}"
                       {required} {pattern} {min_length} {max_length}>
                {icon}
            </div>
        </div>
        """

    @classmethod
    def _render_textarea(cls, element: Dict[str, Any]) -> str:
        """Render a textarea element with Bulma styling."""
        name = element['name']
        required = 'required' if element.get('required', False) else ''
        value = element.get('value', '')
        placeholder = element.get('placeholder', '')
        label = element.get('label', '')
        rows = element.get('rows', 3)
        
        return f"""
        <div class="field">
            <label class="label">{label}</label>
            <div class="control">
                <textarea class="textarea" name="{name}"
                          placeholder="{placeholder}" rows="{rows}"
                          {required}>{value}</textarea>
            </div>
        </div>
        """

    @classmethod
    def _render_select(cls, element: Dict[str, Any]) -> str:
        """Render a select element with Bulma styling."""
        name = element['name']
        required = 'required' if element.get('required', False) else ''
        multiple = 'multiple' if element.get('multiple', False) else ''
        size = f'size="{element["size"]}"' if element.get('size') else ''
        options = element['options']
        label = element.get('label', '')
        
        options_html = '\n'.join(
            f'<option value="{opt["value"]}">{opt["label"]}</option>'
            for opt in options
        )
        
        return f"""
        <div class="field">
            <label class="label">{label}</label>
            <div class="control">
                <div class="select is-fullwidth {' is-multiple' if multiple else ''}">
                    <select name="{name}" {required} {multiple} {size}>
                        <option value="">Select an option</option>
                        {options_html}
                    </select>
                </div>
            </div>
        </div>
        """

    @classmethod
    def _render_radio_group(cls, element: Dict[str, Any]) -> str:
        """Render a group of radio buttons with Bulma styling."""
        name = element['name']
        required = 'required' if element.get('required', False) else ''
        options = element['options']
        default_value = element.get('default_value')
        
        options_html = []
        for opt in options:
            checked = 'checked' if opt['value'] == default_value else ''
            options_html.append(f"""
            <label class="radio">
                <input type="radio" name="{name}" value="{opt['value']}"
                       {required} {checked}>
                {opt['label']}
            </label>
            """)
        
        return f"""
        <div class="field">
            <label class="label">Subscription Plan</label>
            <div class="control radio-group">
                {''.join(options_html)}
            </div>
        </div>
        """

    @classmethod
    def _render_checkbox_group(cls, element: Dict[str, Any]) -> str:
        """Render a group of checkboxes with Bulma styling."""
        name = element['name']
        required = 'required' if element.get('required', False) else ''
        options = element['options']
        min_select = element.get('min_select', 0)
        max_select = element.get('max_select')
        
        checkboxes_html = []
        for opt in options:
            checkboxes_html.append(f"""
            <label class="checkbox">
                <input type="checkbox" name="{name}[]" value="{opt['value']}"
                       {required} data-min-select="{min_select}"
                       {f'data-max-select="{max_select}"' if max_select else ''}>
                {opt['label']}
            </label>
            """)
        
        return f"""
        <div class="field">
            <label class="label">Interests</label>
            <div class="control checkbox-group">
                {''.join(checkboxes_html)}
            </div>
            <p class="help">Select between {min_select} and {max_select if max_select else 'unlimited'} options</p>
        </div>
        """

    @classmethod
    def buildHTML(cls, form_data: HTML5FormData) -> str:
        """Build HTML for form using Bulma CSS classes."""
        form_id = form_data.form_header['form_id']
        method = form_data.form_header['method']
        action = form_data.form_header['action']
        enctype = f'enctype="{form_data.form_header["enctype"]}"' if form_data.form_header["enctype"] else ''
        
        elements_html = []
        for element in form_data.form_elements:
            element_type = element['type']
            
            if element_type == 'input':
                elements_html.append(cls._render_input(element))
            elif element_type == 'textarea':
                elements_html.append(cls._render_textarea(element))
            elif element_type == 'select':
                elements_html.append(cls._render_select(element))
            elif element_type == 'radio_group':
                elements_html.append(cls._render_radio_group(element))
            elif element_type == 'checkbox_group':
                elements_html.append(cls._render_checkbox_group(element))
        
        submit_button = """
        <div class="field">
            <div class="control">
                <button class="button is-primary is-fullwidth" type="submit">
                    <span class="icon">
                        <i class="fas fa-paper-plane"></i>
                    </span>
                    <span>Submit</span>
                </button>
            </div>
        </div>
        """
        
        return f"""
        <form id="{form_id}" method="{method}" action="{action}" {enctype}>
            {''.join(elements_html)}
            {submit_button}
        </form>
        """
