from .abstract import AbstractTemplate

class MaterializeTemplate(AbstractTemplate):
    def __init__(self, form_json):
        super().__init__(form_json)

    def render_text_field(self, field_json):
        return f"""
        <div class="input-field">
            <input id="{field_json['name']}" name="{field_json['name']}" type="text" class="validate">
            <label for="{field_json['name']}">{field_json['label']}</label>
        </div>
        """

    def render_select_field(self, field_json):
        options_html = "".join([f'<option value="{option}">{option}</option>' for option in field_json['options']])
        return f"""
        <div class="input-field">
            <select id="{field_json['name']}" name="{field_json['name']}">
                {options_html}
            </select>
            <label>{field_json['label']}</label>
        </div>
        """

    def render_form(self):
        fields_html = "".join([self.render_field(field) for field in self.form_json['fields']])
        return f"""
        <form action="{self.form_json['action']}" method="{self.form_json['method']}">
            {fields_html}
            <button class="btn waves-effect waves-light" type="submit" name="action">Submit
                <i class="material-icons right">send</i>
            </button>
        </form>
        """

    def render_page(self):
        return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
                <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
            </head>
            <body>
                <div class="container">
                    <h1>{self.form_json['title']}</h1>
                    {self.render_form()}
                </div>
            </body>
        </html>
        """
