from .abstract import AbstractFormTemplate
from ..form_data import HTML5FormData

class MaterializeFormTemplate(AbstractFormTemplate):
    """Form template that generates Materialize CSS styled forms."""
    
    @classmethod
    def buildCSS(cls, form_data: HTML5FormData) -> str:
        """Include Materialize CSS from CDN."""
        return """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        """
    
    @classmethod
    def buildJS(cls, form_data: HTML5FormData) -> str:
        """Include Materialize JavaScript from CDN."""
        return """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                var elems = document.querySelectorAll('select');
                var instances = M.FormSelect.init(elems);
            });
        </script>
        """
    
    @classmethod
    def buildHTML(cls, form_data: HTML5FormData) -> str:
        """Build HTML for form using Materialize CSS classes."""
        form_dict = form_data.to_dict()["form"]
        form_header = form_dict["form_header"]
        elements = form_dict["form_element_list"]
        
        # Start form tag
        html = f'<form id="{form_header["form_id"]}" '
        html += f'method="{form_header["method"]}" '
        if form_header["action"]:
            html += f'action="{form_header["action"]}" '
        if form_header["enctype"]:
            html += f'enctype="{form_header["enctype"]}" '
        html += '>\n'
        
        # Add form elements
        for element in elements:
            html += cls._build_element(element)
        
        # Add submit button
        html += """
        <div class="input-field">
            <button class="btn waves-effect waves-light" type="submit" name="action">
                Submit
                <i class="material-icons right">send</i>
            </button>
        </div>
        """
        
        # Close form
        html += "</form>"
        return html
    
    @classmethod
    def _build_element(cls, element: dict) -> str:
        """Build HTML for a single form element."""
        element_type = element["type"]
        
        if element_type == "input":
            return cls._build_input_element(element)
        elif element_type == "textarea":
            return cls._build_textarea_element(element)
        elif element_type == "select":
            return cls._build_select_element(element)
        elif element_type == "checkbox_group":
            return cls._build_checkbox_group(element)
        elif element_type == "radio_group":
            return cls._build_radio_group(element)
        
        return "<!-- Unsupported element type -->\n"
    
    @classmethod
    def _build_input_element(cls, element: dict) -> str:
        """Build HTML for input elements."""
        input_type = element["input_type"]
        required = 'required' if element.get("required", False) else ''
        label = element.get("label", "")
        name = element["name"]
        placeholder = element.get("placeholder", "")
        value = element.get("value", "")
        pattern = f'pattern="{element["pattern"]}"' if element.get("pattern") else ''
        min_length = f'minlength="{element["min_length"]}"' if element.get("min_length") else ''
        max_length = f'maxlength="{element["max_length"]}"' if element.get("max_length") else ''
        
        if input_type == "checkbox":
            return f"""
            <p>
                <label>
                    <input type="checkbox" name="{name}" {required}/>
                    <span>{label}</span>
                </label>
            </p>
            """
        
        return f"""
        <div class="input-field">
            <input type="{input_type}" id="{name}" name="{name}"
                   value="{value}" {required} {pattern} {min_length} {max_length}>
            <label for="{name}">{label}</label>
        </div>
        """
    
    @classmethod
    def _build_textarea_element(cls, element: dict) -> str:
        """Build HTML for textarea elements."""
        required = 'required' if element.get("required", False) else ''
        name = element["name"]
        label = element.get("label", "")
        value = element.get("value", "")
        
        return f"""
        <div class="input-field">
            <textarea id="{name}" name="{name}"
                      class="materialize-textarea" {required}>{value}</textarea>
            <label for="{name}">{label}</label>
        </div>
        """
    
    @classmethod
    def _build_select_element(cls, element: dict) -> str:
        """Build HTML for select elements."""
        name = element["name"]
        options = element["options"]
        required = 'required' if element.get("required", False) else ''
        label = element.get("label", "")
        
        options_html = "\n".join(
            f'<option value="{opt["value"]}">{opt["label"]}</option>'
            for opt in options
        )
        
        return f"""
        <div class="input-field">
            <select id="{name}" name="{name}" {required}>
                <option value="" disabled selected>Choose your option</option>
                {options_html}
            </select>
            <label>{label}</label>
        </div>
        """
    
    @classmethod
    def _build_checkbox_group(cls, element: dict) -> str:
        """Build HTML for checkbox groups."""
        name = element["name"]
        options = element["options"]
        required = 'required' if element.get("required", False) else ''
        
        checkboxes = []
        for option in options:
            checkboxes.append(f"""
            <p>
                <label>
                    <input type="checkbox" name="{name}[]"
                           value="{option["value"]}" {required}/>
                    <span>{option["label"]}</span>
                </label>
            </p>
            """)
        
        return "\n".join(checkboxes)
    
    @classmethod
    def _build_radio_group(cls, element: dict) -> str:
        """Build HTML for radio groups."""
        name = element["name"]
        options = element["options"]
        required = 'required' if element.get("required", False) else ''
        default_value = element.get("default_value")
        
        radios = []
        for option in options:
            checked = 'checked' if option["value"] == default_value else ''
            radios.append(f"""
            <p>
                <label>
                    <input type="radio" name="{name}"
                           value="{option["value"]}"
                           {required} {checked}/>
                    <span>{option["label"]}</span>
                </label>
            </p>
            """)
        
        return "\n".join(radios)
