import json
from src.durctoo.forms import FormGenerator
from src.durctoo.templates import MaterializeTemplate

example_form_json = {
    "title": "Example Materialize Form",
    "action": "/submit",
    "method": "POST",
    "fields": [
        {
            "type": "text",
            "name": "name",
            "label": "Name"
        },
        {
            "type": "select",
            "name": "color",
            "label": "Favorite Color",
            "options": [
                "Red",
                "Green",
                "Blue"
            ]
        }
    ]
}

form_generator = FormGenerator(example_form_json, MaterializeTemplate)
generated_form = form_generator.generate_form()

print("Generated Materialize Form:")
print(generated_form)

with open("example_output/materialize_form.html", "w") as f:
    f.write(generated_form)
