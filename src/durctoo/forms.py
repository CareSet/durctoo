from typing import Union, Type
from .form_data import HTML5FormData
from .templates import AbstractFormTemplate

class FormGenerator:
    """Generator for HTML forms using various templates."""
    
    def __init__(self, form_data: Union[str, dict], template_class: Type[AbstractFormTemplate]):
        """Initialize the form generator.
        
        Args:
            form_data: Either a file path to a JSON file, a JSON string, or a dictionary
                      containing the form data
            template_class: The template class to use for generating the form
        """
        self.form_data = HTML5FormData.create_from_json(form_data)
        self.template_class = template_class

    def generate_form(self) -> str:
        """Generate the complete HTML form.
        
        Returns:
            str: The complete HTML form including CSS, HTML, and JavaScript
        """
        css, html, js = self.template_class.buildForm(self.form_data)
        return f"""<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{self.form_data.to_dict()['form']['form_header']['form_id']}</title>
        {css}
    </head>
    <body>
        <div class="container">
            {html}
        </div>
        {js}
    </body>
</html>"""
